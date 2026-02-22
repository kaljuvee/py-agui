"""
py-agui: Simple Chat Example

Minimal streaming chat with an AI agent. No state, no tools - just chat.

Run: python examples/simple_chat.py
"""
from fasthtml.common import *
from pydantic_ai import Agent
from py_agui import setup_agui
from py_agui.layouts import simple_chat

app, rt = fast_app(exts='ws', hdrs=[MarkdownJS()])

agent = Agent('openai:gpt-4o-mini', instructions='Be helpful and concise.')
agui = setup_agui(app, agent)


@rt('/')
def index():
    return simple_chat(agui.chat("main"))


if __name__ == "__main__":
    serve()
