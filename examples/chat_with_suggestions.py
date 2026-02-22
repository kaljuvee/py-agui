"""
py-agui: Chat with Suggestion Buttons

Demonstrates dynamic suggestion buttons that update based on conversation context.

Run: python examples/chat_with_suggestions.py
"""
from fasthtml.common import *
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext, ToolReturn
from pydantic_ai.ui import StateDeps
from py_agui import setup_agui
from py_agui.layouts import three_pane_layout
from typing import List

agui_ref = None


class UserState(BaseModel):
    current_topic: str = "General"

    def __ft__(self):
        return Div(
            P(f"Topic: {self.current_topic}", style="font-weight:500;font-size:0.85rem;"),
            id="agui-state"
        )


agent = Agent[StateDeps[UserState]](
    'openai:gpt-4o-mini',
    instructions='You are a helpful assistant. Before finishing, use anticipate_questions to suggest follow-ups. Keep suggestions short.',
    deps_type=StateDeps[UserState]
)


@agent.tool
async def anticipate_questions(ctx: RunContext[StateDeps[UserState]], questions: List[str]) -> ToolReturn:
    """Set suggestion buttons for follow-up questions."""
    if agui_ref:
        await agui_ref.set_suggestions("main", questions[:4])
    return ToolReturn(return_value=f"Set {len(questions)} suggestions")


app, rt = fast_app(exts='ws', hdrs=[MarkdownJS()])
agui = setup_agui(app, agent, UserState(), UserState)
agui_ref = agui


@rt('/')
async def index():
    await agui.set_suggestions("main", [
        "What can you help with?",
        "Tell me a joke",
        "Explain quantum computing",
        "Write a haiku"
    ])
    return three_pane_layout(
        chat_component=agui.chat("main"),
        state_component=agui.state("main"),
        title="Chat with Suggestions"
    )


if __name__ == "__main__":
    serve()
