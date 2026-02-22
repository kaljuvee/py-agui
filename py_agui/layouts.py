"""Pre-built layout components including the 3-pane agentic UI."""
from fasthtml.common import *
from .styles import get_chat_styles, get_custom_theme


def chat_with_sidebar(chat_component, sidebar_component, **kwargs):
    """Standard 2-column layout: sidebar + chat."""
    return Div(
        get_chat_styles(),
        Div(
            Div(sidebar_component, cls="chat-layout-sidebar"),
            Div(chat_component, cls="chat-layout-main"),
            cls="chat-layout"
        ),
        **kwargs
    )


def simple_chat(chat_component, **kwargs):
    """Full-width chat layout."""
    return Div(
        get_chat_styles(),
        Div(chat_component, style="height: 100vh; padding: 1rem;"),
        **kwargs
    )


def three_pane_layout(
    chat_component,
    settings_component=None,
    state_component=None,
    title="py-agui",
    **kwargs
):
    """
    3-pane agentic UI layout:
    - Left: settings panel
    - Center: streaming chat
    - Right: thinking trace (on-demand slide-out panel)

    Args:
        chat_component: The chat component (agui.chat())
        settings_component: Left pane settings (or None for defaults)
        state_component: Optional state display in settings pane
        title: Header title
    """
    # Default settings panel
    if settings_component is None:
        settings_component = Div(
            H2("Settings"),
            Div(
                Label("Model"),
                Select(
                    Option("openai:gpt-4o-mini", value="openai:gpt-4o-mini"),
                    Option("openai:gpt-4o", value="openai:gpt-4o"),
                    Option("anthropic:claude-sonnet-4-20250514", value="anthropic:claude-sonnet-4-20250514"),
                    id="model-select", name="model"
                ),
                cls="setting-group"
            ),
            Hr(cls="setting-divider"),
            Div(
                Label("System Prompt"),
                Textarea(
                    "You are a helpful assistant.",
                    id="system-prompt", name="system_prompt",
                    rows="4", style="resize: vertical;"
                ),
                cls="setting-group"
            ),
            Hr(cls="setting-divider"),
            Div(
                Label("Temperature"),
                Input(type="number", id="temperature", name="temperature",
                      value="0.7", min="0", max="2", step="0.1"),
                cls="setting-group"
            ),
        )

    # Thinking trace panel (slide-out from right)
    thinking_panel = Div(
        Div(
            H3("Thinking Trace"),
            Button("x", cls="agui-thinking-close",
                   onclick="document.getElementById('thinking-panel').classList.remove('open');document.getElementById('think-btn').classList.remove('active');"),
            cls="agui-thinking-header"
        ),
        Div(id="thinking-steps", cls="agui-thinking-content"),
        id="thinking-panel",
        cls="agui-thinking-overlay"
    )

    # Header bar with thinking toggle
    header = Div(
        Span(title, cls="agui-header-title"),
        Div(
            Span("0", id="thinking-badge", cls="agui-think-badge"),
            Button(
                "Thinking",
                id="think-btn",
                cls="agui-think-btn",
                onclick="const p=document.getElementById('thinking-panel');const b=this;p.classList.toggle('open');b.classList.toggle('active');"
            ),
            cls="agui-header-actions"
        ),
        cls="agui-header"
    )

    # Update badge script
    badge_script = Script("""
        function updateThinkingBadge(count) {
            const badge = document.getElementById('thinking-badge');
            if (badge) badge.textContent = count;
        }
    """)

    return Div(
        get_chat_styles(),
        badge_script,
        Div(
            # Left: settings
            Div(
                settings_component,
                Hr(cls="setting-divider") if state_component else "",
                Div(id="agui-state", children=[state_component] if state_component else []),
                cls="agui-settings"
            ),
            # Center: header + chat
            Div(
                header,
                chat_component,
                cls="agui-main"
            ),
            cls="agui-app"
        ),
        thinking_panel,
        **kwargs
    )
