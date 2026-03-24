from settings import *
from notion_api import NotionClient
from clean_ollama import Client, Message, Role
from rich.panel import Panel
from rich.markdown import Markdown


class LangEngine:
    def __init__(self, token, model):
        self.notion = NotionClient(token)
        self.notion.sync()
        self.notes = self.notion.get_notes()
        self.ollama = Client(model)
        self.history = []

    def read_note(self, id: int) -> str:
        title = self.notes[id]["title"]

        CONSOLE.print(Panel(
            f"{title}",
            title="Reading note",
            title_align="left",
            border_style="",
            expand=False
        ))

        return self.notes[id]["content"]

    def get_structure(self) -> str:
        index = self.get_index()
        CONSOLE.print(Panel(
            f"{index}",
            title="Read structure",
            title_align="left",
            border_style="",
            expand=False
        ))

        return index

    def dispatch(self, tool_call) -> str:
        name = tool_call.function.name
        args = tool_call.function.arguments
        handlers = {
            "read_note": lambda: self.read_note(args["id"]),
            "get_structure": lambda: self.get_structure()
        }
        return handlers[name]()

    def get_index(self) -> str:
        lines = []
        for id, note in self.notes.items():
            indent = "  " * self._depth(id)
            children = note["children"]
            lines.append(f"{indent}[{id}] {note['title']}" + (f" (children: {children})" if children else ""))
        return "\n".join(lines)

    def _depth(self, id: int) -> int:
        depth = 0
        current = self.notes[id]
        while current["parent"] is not None:
            current = self.notes[current["parent"]]
            depth += 1
        return depth

    def chat(self, user_message: str) -> str:
        if not self.history:
            self.history.append(Message(Role.SYSTEM, SYSTEM_PROMPT))

        self.history.append(Message(Role.USER, user_message))
        thinking, response, tool_calls = self.ollama.generate(self.history, tools=TOOLS)

        if thinking:
            CONSOLE.print(Markdown(f"> *{thinking}*\n"))

        while tool_calls:
            for tool_call in tool_calls:
                result = self.dispatch(tool_call)
                self.history.append(Message(Role.ASSISTANT, str(result)))
                self.history.append(Message(Role.TOOL, str(result)))

            thinking, response, tool_calls = self.ollama.generate(self.history, tools=TOOLS)

            if thinking:
                CONSOLE.print(Markdown(f"> *{thinking}*\n"))

        self.history.append(Message(Role.ASSISTANT, response))
        return response
