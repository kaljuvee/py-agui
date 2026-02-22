"""
py-agui: Chat with State Management

Demonstrates state management with agent tools and pydantic UI rendering.
The agent can take notes organized by category, with live state updates.

Run: python examples/chat_with_state.py
"""
from fasthtml.common import *
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, ToolReturn
from pydantic_ai.ui import StateDeps
from ag_ui.core.events import StateSnapshotEvent, EventType
from py_agui import setup_agui
from py_agui.layouts import chat_with_sidebar
from typing import List, Dict


class Note(BaseModel):
    id: str
    title: str
    content: str

    def __ft__(self):
        return Li(
            Card(
                Div(self.content, cls="marked prose prose-sm"),
                header=H4(self.title)
            )
        )


class ChatState(BaseModel):
    notes: Dict[str, List[Note]] = Field(default_factory=dict)
    current_topic: str = "General"

    def __ft__(self):
        return Card(
            Card(
                *[Div(H4(cat), Ul(*[Li(note) for note in notes])) for cat, notes in self.notes.items()],
                header=H3("Notes")
            ) if self.notes else P("No notes yet. Ask me to take notes!", style="color:#94a3b8;font-style:italic;"),
            header=H2(self.current_topic),
            id="agui-state"
        )


agent = Agent[StateDeps[ChatState]](
    'openai:gpt-4o-mini',
    instructions='You are a helpful assistant that takes notes. Use tools to manage notes and topics.',
    deps_type=StateDeps[ChatState]
)


@agent.tool
def add_note(ctx: RunContext[StateDeps[ChatState]], category: str, title: str, content: str) -> ToolReturn:
    """Add a note to a category."""
    import uuid
    note = Note(id=str(uuid.uuid4()), title=title, content=content)
    ctx.deps.state.notes.setdefault(category, []).append(note)
    return ToolReturn(
        return_value=f"Added note: {title}",
        metadata=[StateSnapshotEvent(type=EventType.STATE_SNAPSHOT, snapshot=ctx.deps.state)]
    )


@agent.tool
def set_topic(ctx: RunContext[StateDeps[ChatState]], topic: str) -> ToolReturn:
    """Set the current conversation topic."""
    ctx.deps.state.current_topic = topic
    return ToolReturn(
        return_value=f"Topic set to: {topic}",
        metadata=[StateSnapshotEvent(type=EventType.STATE_SNAPSHOT, snapshot=ctx.deps.state)]
    )


@agent.tool
def list_notes(ctx: RunContext[StateDeps[ChatState]], category: str = "") -> str:
    """List notes, optionally filtered by category."""
    notes = ctx.deps.state.notes
    if not notes:
        return "No notes found."
    if category and category in notes:
        return "\n".join(f"- {n.title}: {n.content}" for n in notes[category])
    return "\n".join(
        f"[{cat}] {n.title}: {n.content}"
        for cat, ns in notes.items() for n in ns
    )


app, rt = fast_app(exts='ws', hdrs=[MarkdownJS()])
agui = setup_agui(app, agent, ChatState(), ChatState)


@rt('/')
def index():
    return chat_with_sidebar(
        chat_component=agui.chat("main"),
        sidebar_component=agui.state("main")
    )


if __name__ == "__main__":
    serve()
