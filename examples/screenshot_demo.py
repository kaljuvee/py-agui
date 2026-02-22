"""
Static demo for screenshots - shows the full 3-pane layout with sample data.
No LLM API key required.

Run: python examples/screenshot_demo.py
"""
from fasthtml.common import *
from py_agui.styles import get_chat_styles


app, rt = fast_app(hdrs=[MarkdownJS()])


def sample_message(role, content, msg_id=""):
    cls = "chat-user" if role == "user" else "chat-assistant"
    return Div(
        Div(content, cls="chat-message-content marked"),
        cls=f"chat-message {cls}",
        id=msg_id
    )


def sample_tool_msg(name):
    return Div(
        Div(f"Using {name}...", cls="chat-message-content"),
        cls="chat-message chat-tool"
    )


@rt('/')
def index():
    # Settings panel
    settings = Div(
        H2("py-agui"),
        P("Python Agentic UI", style="font-size:0.8rem;color:#64748b;margin:0 0 1rem 0;"),
        Hr(cls="setting-divider"),
        Div(
            Label("Model"),
            Select(
                Option("openai:gpt-4o-mini", selected=True),
                Option("openai:gpt-4o"),
                Option("anthropic:claude-sonnet-4-20250514"),
                id="model-select"
            ),
            cls="setting-group"
        ),
        Hr(cls="setting-divider"),
        Div(
            Label("Temperature"),
            Input(type="number", value="0.7", min="0", max="2", step="0.1"),
            cls="setting-group"
        ),
        Hr(cls="setting-divider"),
        Div(
            Label("System Prompt"),
            Textarea("You are a helpful assistant that manages contacts and tasks.",
                     rows="3", style="resize:vertical;"),
            cls="setting-group"
        ),
        Hr(cls="setting-divider"),
        # State section
        Div(
            H4("Contacts", style="margin:0 0 0.5rem 0;font-size:0.85rem;color:#3b82f6;"),
            Div(
                Div(
                    Div("A", style="width:2rem;height:2rem;border-radius:50%;background:#3b82f6;color:white;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:0.8rem;"),
                    Div(
                        Div("Alice Chen", style="font-weight:500;font-size:0.85rem;"),
                        Div("Engineering Lead", style="font-size:0.75rem;color:#64748b;"),
                    ),
                    style="display:flex;gap:0.5rem;align-items:center;"
                ),
                cls="pydantic-ui-card", style="padding:0.6rem 0.8rem;"
            ),
            Div(
                Div(
                    Div("B", style="width:2rem;height:2rem;border-radius:50%;background:#3b82f6;color:white;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:0.8rem;"),
                    Div(
                        Div("Bob Smith", style="font-weight:500;font-size:0.85rem;"),
                        Div("Product Manager", style="font-size:0.75rem;color:#64748b;"),
                    ),
                    style="display:flex;gap:0.5rem;align-items:center;"
                ),
                cls="pydantic-ui-card", style="padding:0.6rem 0.8rem;"
            ),
            style="margin-bottom:0.75rem;"
        ),
        Div(
            H4("Tasks", style="margin:0 0 0.5rem 0;font-size:0.85rem;color:#f59e0b;"),
            Div(
                Div(Span("[x]", style="font-family:monospace;color:#22c55e;font-weight:600;margin-right:0.5rem;"),
                    Span("Review PR #42", style="text-decoration:line-through;color:#94a3b8;font-size:0.85rem;"),
                    style="display:flex;align-items:center;"),
                cls="pydantic-ui-field"
            ),
            Div(
                Div(Span("[ ]", style="font-family:monospace;color:#ef4444;font-weight:600;margin-right:0.5rem;"),
                    Span("Deploy v2.0 to staging", style="font-size:0.85rem;"),
                    style="display:flex;align-items:center;"),
                cls="pydantic-ui-field"
            ),
            Div(
                Div(Span("[ ]", style="font-family:monospace;color:#f59e0b;font-weight:600;margin-right:0.5rem;"),
                    Span("Write API documentation", style="font-size:0.85rem;"),
                    style="display:flex;align-items:center;"),
                cls="pydantic-ui-field"
            ),
            cls="pydantic-ui-card"
        ),
    )

    # Chat messages
    messages = Div(
        sample_message("user", "Can you add Alice Chen as a contact? She's the engineering lead."),
        sample_tool_msg("add_contact"),
        sample_message("assistant",
                       "I've added **Alice Chen** as a contact with the role of Engineering Lead. "
                       "You can see her in the contacts panel on the left. Would you like to add anyone else?"),
        sample_message("user", "Add a high priority task: Deploy v2.0 to staging"),
        sample_tool_msg("add_task"),
        sample_message("assistant",
                       "Done! I've added **Deploy v2.0 to staging** as a high-priority task. "
                       "I can see you also have a completed PR review and a pending documentation task. "
                       "Need anything else?"),
        id="chat-messages",
        cls="chat-messages"
    )

    # Suggestion buttons
    suggestions = Div(
        Button("Add another contact", cls="suggestion-btn"),
        Button("Show all tasks", cls="suggestion-btn"),
        Button("Set a summary", cls="suggestion-btn"),
        Button("Complete a task", cls="suggestion-btn"),
        id="suggestion-buttons"
    )

    # Input form
    input_form = Div(
        suggestions,
        Div(id="chat-status", cls="chat-status"),
        Form(
            Textarea(placeholder="Type a message...", cls="chat-input-field", rows="1"),
            Button("Send", type="submit", cls="chat-input-button"),
            cls="chat-input-form"
        ),
        cls="chat-input"
    )

    # Thinking panel (open by default for screenshot)
    thinking_panel = Div(
        Div(
            H3("Thinking Trace"),
            Button("x", cls="agui-thinking-close",
                   onclick="document.getElementById('thinking-panel').classList.remove('open');document.getElementById('think-btn').classList.remove('active');"),
            cls="agui-thinking-header"
        ),
        Div(
            Div(
                Div("Tool Call", cls="thinking-step-header"),
                Div("add_contact(name='Alice Chen', role='Engineering Lead')", cls="thinking-step-body"),
                cls="thinking-step tool-call"
            ),
            Div(
                Div("Reasoning", cls="thinking-step-header"),
                Div("The user wants to add a contact. I'll use the add_contact tool with the name and role provided.", cls="thinking-step-body"),
                cls="thinking-step reasoning"
            ),
            Div(
                Div("Tool Call", cls="thinking-step-header"),
                Div("add_task(task='Deploy v2.0 to staging', priority='high')", cls="thinking-step-body"),
                cls="thinking-step tool-call"
            ),
            Div(
                Div("Reasoning", cls="thinking-step-header"),
                Div("User wants a high priority deployment task. Adding it and noting the existing tasks in state.", cls="thinking-step-body"),
                cls="thinking-step reasoning"
            ),
            id="thinking-steps",
            cls="agui-thinking-content"
        ),
        id="thinking-panel",
        cls="agui-thinking-overlay open"
    )

    # Header
    header = Div(
        Span("py-agui Demo", cls="agui-header-title"),
        Div(
            Span("4", id="thinking-badge", cls="agui-think-badge"),
            Button("Thinking", id="think-btn", cls="agui-think-btn active",
                   onclick="const p=document.getElementById('thinking-panel');const b=this;p.classList.toggle('open');b.classList.toggle('active');"),
            cls="agui-header-actions"
        ),
        cls="agui-header"
    )

    # Markdown rendering script
    md_script = Script("""
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('.marked').forEach(el => {
                if (window.marked) el.innerHTML = marked.parse(el.textContent || '');
            });
        });
    """)

    return Div(
        get_chat_styles(),
        md_script,
        Div(
            Div(settings, cls="agui-settings"),
            Div(
                header,
                Div(messages, input_form, cls="chat-container"),
                cls="agui-main"
            ),
            cls="agui-app"
        ),
        thinking_panel
    )


if __name__ == "__main__":
    serve()
