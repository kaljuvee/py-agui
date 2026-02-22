"""
py-agui: 3-Pane Agentic UI Demo

Left pane:  Settings (model, system prompt, temperature)
Mid pane:   Streaming chat with pydantic-ai UI components
Right pane: Thinking trace (on-demand slide-out)

Run: python examples/three_pane_demo.py
"""
from fasthtml.common import *
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, ToolReturn
from pydantic_ai.ui import StateDeps
from ag_ui.core.events import StateSnapshotEvent, EventType
from py_agui import setup_agui
from py_agui.layouts import three_pane_layout
from typing import List, Dict
import uuid


# --- Pydantic models for state & UI components ---

class Contact(BaseModel):
    name: str
    email: str = ""
    role: str = ""

    def __ft__(self):
        return Div(
            Div(
                Div(self.name[0].upper(),
                    style="width:2rem;height:2rem;border-radius:50%;background:#3b82f6;color:white;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:0.8rem;"),
                Div(
                    Div(self.name, style="font-weight:500;font-size:0.85rem;"),
                    Div(self.role, style="font-size:0.75rem;color:#64748b;") if self.role else "",
                    Div(self.email, style="font-size:0.75rem;color:#64748b;") if self.email else "",
                ),
                style="display:flex;gap:0.5rem;align-items:center;"
            ),
            cls="pydantic-ui-card",
            style="padding:0.6rem 0.8rem;"
        )


class TodoItem(BaseModel):
    task: str
    done: bool = False
    priority: str = "medium"

    def __ft__(self):
        colors = {"high": "#ef4444", "medium": "#f59e0b", "low": "#22c55e"}
        color = colors.get(self.priority, "#64748b")
        check = "x" if self.done else " "
        text_style = "text-decoration:line-through;color:#94a3b8;" if self.done else ""
        return Div(
            Div(
                Span(f"[{check}]", style=f"font-family:monospace;color:{color};font-weight:600;margin-right:0.5rem;"),
                Span(self.task, style=text_style + "font-size:0.85rem;"),
                style="display:flex;align-items:center;"
            ),
            cls="pydantic-ui-field"
        )


class AppState(BaseModel):
    """Application state rendered as pydantic UI components in the settings pane."""
    contacts: List[Contact] = Field(default_factory=list)
    todos: List[TodoItem] = Field(default_factory=list)
    summary: str = ""

    def __ft__(self):
        sections = []
        if self.contacts:
            sections.append(Div(
                H4("Contacts", style="margin:0 0 0.5rem 0;font-size:0.85rem;color:#3b82f6;"),
                *[c.__ft__() for c in self.contacts],
                style="margin-bottom:0.75rem;"
            ))
        if self.todos:
            sections.append(Div(
                H4("Tasks", style="margin:0 0 0.5rem 0;font-size:0.85rem;color:#f59e0b;"),
                *[t.__ft__() for t in self.todos],
                cls="pydantic-ui-card"
            ))
        if self.summary:
            sections.append(Div(
                H4("Summary", style="margin:0 0 0.5rem 0;font-size:0.85rem;color:#8b5cf6;"),
                P(self.summary, style="font-size:0.825rem;margin:0;color:#475569;"),
                cls="pydantic-ui-card"
            ))
        if not sections:
            sections.append(P("Chat with the assistant to build contacts, tasks, and more.",
                              style="font-size:0.825rem;color:#94a3b8;font-style:italic;"))
        return Div(*sections, id="agui-state", hx_swap_oob="innerHTML")


# --- Agent with tools ---

agent = Agent[StateDeps[AppState]](
    'openai:gpt-4o-mini',
    instructions="""You are a helpful assistant that can manage contacts, tasks, and summaries.
Use the provided tools to add contacts, tasks, or set a summary based on user requests.
Be concise and friendly. When you use tools, the UI will update automatically.""",
    deps_type=StateDeps[AppState]
)


@agent.tool
def add_contact(ctx: RunContext[StateDeps[AppState]], name: str, email: str = "", role: str = "") -> ToolReturn:
    """Add a contact to the list."""
    contact = Contact(name=name, email=email, role=role)
    ctx.deps.state.contacts.append(contact)
    return ToolReturn(
        return_value=f"Added contact: {name}",
        metadata=[StateSnapshotEvent(type=EventType.STATE_SNAPSHOT, snapshot=ctx.deps.state)]
    )


@agent.tool
def add_task(ctx: RunContext[StateDeps[AppState]], task: str, priority: str = "medium") -> ToolReturn:
    """Add a task/todo item. Priority: high, medium, or low."""
    item = TodoItem(task=task, priority=priority)
    ctx.deps.state.todos.append(item)
    return ToolReturn(
        return_value=f"Added task: {task} ({priority} priority)",
        metadata=[StateSnapshotEvent(type=EventType.STATE_SNAPSHOT, snapshot=ctx.deps.state)]
    )


@agent.tool
def complete_task(ctx: RunContext[StateDeps[AppState]], task_index: int) -> ToolReturn:
    """Mark a task as complete by its index (0-based)."""
    if 0 <= task_index < len(ctx.deps.state.todos):
        ctx.deps.state.todos[task_index].done = True
        return ToolReturn(
            return_value=f"Completed task: {ctx.deps.state.todos[task_index].task}",
            metadata=[StateSnapshotEvent(type=EventType.STATE_SNAPSHOT, snapshot=ctx.deps.state)]
        )
    return ToolReturn(return_value="Task index out of range")


@agent.tool
def set_summary(ctx: RunContext[StateDeps[AppState]], summary: str) -> ToolReturn:
    """Set a brief summary note."""
    ctx.deps.state.summary = summary
    return ToolReturn(
        return_value=f"Summary set",
        metadata=[StateSnapshotEvent(type=EventType.STATE_SNAPSHOT, snapshot=ctx.deps.state)]
    )


@agent.tool
def list_all(ctx: RunContext[StateDeps[AppState]]) -> str:
    """List all contacts and tasks."""
    parts = []
    if ctx.deps.state.contacts:
        parts.append("Contacts: " + ", ".join(c.name for c in ctx.deps.state.contacts))
    if ctx.deps.state.todos:
        parts.append("Tasks: " + ", ".join(
            f"{'[x]' if t.done else '[ ]'} {t.task}" for t in ctx.deps.state.todos
        ))
    if ctx.deps.state.summary:
        parts.append(f"Summary: {ctx.deps.state.summary}")
    return "\n".join(parts) if parts else "Nothing stored yet."


# --- FastHTML App ---

app, rt = fast_app(exts='ws', hdrs=[MarkdownJS()])
agui = setup_agui(app, agent, AppState(), AppState)

THREAD = "main"


@rt('/')
def index():
    # Custom settings panel
    settings = Div(
        H2("py-agui"),
        P("Python Agentic UI", style="font-size:0.8rem;color:#64748b;margin:0 0 1rem 0;"),
        Hr(cls="setting-divider"),
        Div(
            Label("Model"),
            Select(
                Option("openai:gpt-4o-mini", value="openai:gpt-4o-mini", selected=True),
                Option("openai:gpt-4o", value="openai:gpt-4o"),
                Option("anthropic:claude-sonnet-4-20250514", value="anthropic:claude-sonnet-4-20250514"),
                id="model-select"
            ),
            cls="setting-group"
        ),
        Hr(cls="setting-divider"),
        Div(
            Label("Temperature"),
            Input(type="number", value="0.7", min="0", max="2", step="0.1", id="temperature"),
            cls="setting-group"
        ),
        Hr(cls="setting-divider"),
        Div(
            Label("System Prompt"),
            Textarea("You are a helpful assistant that manages contacts and tasks.",
                     rows="3", id="system-prompt", style="resize:vertical;"),
            cls="setting-group"
        ),
    )

    return three_pane_layout(
        chat_component=agui.chat(THREAD),
        settings_component=settings,
        state_component=agui.state(THREAD),
        title="py-agui Demo"
    )


if __name__ == "__main__":
    serve()
