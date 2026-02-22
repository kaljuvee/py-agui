"""
Patches to add FastHTML rendering (__ft__) methods to ag_ui protocol types.
Includes support for reasoning/thinking trace events.
"""
from fasthtml.common import *
from ag_ui.core.types import BaseMessage
from ag_ui.core.events import (
    TextMessageStartEvent,
    TextMessageContentEvent,
    TextMessageEndEvent,
    TextMessageChunkEvent,
    ToolCallStartEvent,
    ToolCallEndEvent,
    StateSnapshotEvent,
    RunStartedEvent,
    RunFinishedEvent,
    RunErrorEvent,
    StepStartedEvent,
    StepFinishedEvent,
)

# Try importing reasoning events (may not be available in older ag-ui versions)
try:
    from ag_ui.core.events import (
        ReasoningMessageStartEvent,
        ReasoningMessageContentEvent,
        ReasoningMessageEndEvent,
    )
    HAS_REASONING = True
except ImportError:
    HAS_REASONING = False


def setup_ft_patches():
    """Setup FastHTML rendering patches for ag_ui types"""

    @patch
    def __ft__(self: BaseMessage):
        message_class = "chat-user" if self.role == "user" else "chat-assistant"
        return Div(
            Div(self.content, cls="chat-message-content marked"),
            cls=f"chat-message {message_class}",
            id=self.id
        )

    @patch
    def __ft__(self: RunStartedEvent):
        return Div(
            Div(id=f"run-{self.run_id}"),
            id="agui-messages",
            hx_swap_oob="beforeend"
        )

    @patch
    def __ft__(self: TextMessageStartEvent):
        return Div(
            Div(
                Div(
                    Span("", id=f"message-content-{self.message_id}", cls="marked"),
                    Span("", cls="chat-streaming", id=f"streaming-{self.message_id}"),
                    cls="chat-message-content"
                ),
                cls="chat-message chat-assistant",
                id=f"message-{self.message_id}"
            ),
            id="chat-messages",
            hx_swap_oob="beforeend"
        )

    @patch
    def __ft__(self: TextMessageChunkEvent):
        return Span(
            self.delta,
            id=f"message-content-{self.message_id}",
            hx_swap_oob="beforeend"
        )

    @patch
    def __ft__(self: TextMessageContentEvent):
        return Span(
            self.delta,
            id=f"message-content-{self.message_id}",
            hx_swap_oob="beforeend"
        )

    @patch
    def __ft__(self: TextMessageEndEvent):
        return Span("", id=f"streaming-{self.message_id}")

    @patch
    def __ft__(self: StateSnapshotEvent):
        if hasattr(self.snapshot, '__ft__'):
            return self.snapshot.__ft__()
        return Div(
            Pre(str(self.snapshot)),
            id="agui-state",
            hx_swap_oob="innerHTML"
        )

    @patch
    def __ft__(self: ToolCallStartEvent):
        # Render in chat as compact tool indicator
        chat_el = Div(
            Div(
                Div(f"Using {self.tool_call_name}...", cls="chat-message-content"),
                cls="chat-message chat-tool",
                id=f"tool-{self.tool_call_id}"
            ),
            id="chat-messages",
            hx_swap_oob="beforeend"
        )
        # Also add to thinking trace
        thinking_el = Div(
            Div(
                Div("Tool Call", cls="thinking-step-header"),
                Div(f"{self.tool_call_name}", cls="thinking-step-body thinking-streaming",
                    id=f"thinking-tool-{self.tool_call_id}"),
                cls="thinking-step tool-call"
            ),
            id="thinking-steps",
            hx_swap_oob="beforeend"
        )
        return Div(chat_el, thinking_el)

    @patch
    def __ft__(self: ToolCallEndEvent):
        return Div(
            Span("Done", id=f"thinking-tool-{self.tool_call_id}",
                 cls="thinking-step-body", hx_swap_oob="innerHTML"),
        )

    @patch
    def __ft__(self: RunErrorEvent):
        return Div(
            Div(
                Div("Error", cls="thinking-step-header"),
                Div(self.message, cls="thinking-step-body"),
                cls="thinking-step",
                style="border-left-color: #ef4444;"
            ),
            id="thinking-steps",
            hx_swap_oob="beforeend"
        )

    @patch
    def __ft__(self: StepStartedEvent):
        return Div(
            Div(
                Div("Step", cls="thinking-step-header"),
                Div(self.step_name, cls="thinking-step-body thinking-streaming",
                    id=f"thinking-step-{self.step_name}"),
                cls="thinking-step"
            ),
            id="thinking-steps",
            hx_swap_oob="beforeend"
        )

    @patch
    def __ft__(self: StepFinishedEvent):
        return Span("Done", id=f"thinking-step-{self.step_name}",
                     cls="thinking-step-body", hx_swap_oob="innerHTML")

    # Patch reasoning events if available
    if HAS_REASONING:
        @patch
        def __ft__(self: ReasoningMessageStartEvent):
            return Div(
                Div(
                    Div("Reasoning", cls="thinking-step-header"),
                    Div("", cls="thinking-step-body thinking-streaming",
                        id=f"thinking-reason-{self.message_id}"),
                    cls="thinking-step reasoning"
                ),
                id="thinking-steps",
                hx_swap_oob="beforeend"
            )

        @patch
        def __ft__(self: ReasoningMessageContentEvent):
            return Span(
                self.delta,
                id=f"thinking-reason-{self.message_id}",
                hx_swap_oob="beforeend"
            )

        @patch
        def __ft__(self: ReasoningMessageEndEvent):
            return Span("", cls="thinking-step-body",
                         id=f"thinking-reason-done-{self.message_id}")
