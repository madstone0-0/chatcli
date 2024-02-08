import json

# from icecream import ic
from nltk.tokenize import word_tokenize
from prompt_toolkit import PromptSession
from typer import Exit

from chatcli import ENV, EXIT_COMMANDS, con
from chatcli.model import Model

if ENV == "DEBUG":
    from icecream import ic

    ic("Debug Mode")


def load_log(log: str) -> list:
    prompts = []
    try:
        with open(f"{log}", mode="r", encoding="utf-8") as f:
            if f:
                prompts = json.loads(" ".join(f.readlines()))
    except FileNotFoundError:
        return prompts
    return prompts


def read_prompt(session: PromptSession, model: Model):
    prompt = session.prompt(
        f"[{model.nickname}]> ",
        multiline=True,
        prompt_continuation=f"[{model.nickname}]> ",
    )
    if prompt in EXIT_COMMANDS:
        con.print("Exiting...")
        raise Exit(0)
    if isinstance(prompt, list):
        prompt = "\n".join(prompt)
    return prompt


def get_tokens(prompt: str):
    tokens = word_tokenize(prompt)
    return tokens


def generate_prompt(prompt: str):
    return f"""{prompt}"""
