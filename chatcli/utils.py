import json

from nltk.tokenize import word_tokenize
from chatcli import con
from typer import Exit


def load_log(log: str) -> list:
    prompts = []
    try:
        with open(f"{log}", mode="r", encoding="utf-8") as f:
            if f:
                prompts = json.loads(" ".join(f.readlines()))
    except FileNotFoundError:
        return prompts
    return prompts


def read_prompt():
    prompt = []
    # https://stackoverflow.com/a/38223253/9784169
    while True:
        try:
            line = con.input("[green]>[/green] ")
            if line == "exit" or line == "q":
                con.print("Exiting...")
                raise Exit()
        except EOFError:
            break
        prompt.append(line)
    prompt = "\n".join(prompt)
    # https://stackoverflow.com/a/38223253/9784169
    return prompt


def get_tokens(prompt: str):
    tokens = word_tokenize(prompt)
    return tokens


def generate_prompt(prompt: str):
    return f"""{prompt}"""
