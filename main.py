from settings import *
from lang_engine import LangEngine
from rich.markdown import Markdown
from dotenv import load_dotenv
from getpass import getpass
import os


def print_logo():
    CONSOLE.print(f"{LOGO} ({VERSION}) by {AUTHOR}")


def main():
    load_dotenv()
    token = os.getenv("NOTION_TOKEN")
    model = os.getenv("OLLAMA_MODEL")

    if not token:
        token = getpass("Notion token: ")
    if not model:
        model = input("Ollama model: ")

    if not os.getenv("NOTION_TOKEN") or not os.getenv("OLLAMA_MODEL"):
        with open(".env", "w") as f:
            f.write(f"NOTION_TOKEN={token}\n")
            f.write(f"OLLAMA_MODEL={model}\n")

    engine = LangEngine(token, model)

    while True:
        CONSOLE.print()
        user_input = input("> ").strip()

        if user_input.lower() == "/exit":
            engine.ollama.unload()
            break
        if not user_input:
            continue

        CONSOLE.print()
        response = engine.chat(user_input)
        CONSOLE.print(Markdown(f"{response}\n"))


print_logo()
main()
