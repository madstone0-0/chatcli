#!/usr/bin/python3.11
import json
import os
from importlib.metadata import version
from typing import Optional

import openai
import typer
from appdirs import user_data_dir
from nltk.tokenize import word_tokenize
from openai.error import APIConnectionError, RateLimitError
from rich.console import Console

# from icecream import ic


appname = "ChatCli"
appauthor = "madstone0-0"
appdata_location = user_data_dir(appname, appauthor)
os.makedirs(appdata_location, exist_ok=True)

openai.api_key = os.getenv("OPENAI_API_KEY")
app = typer.Typer()
con = Console()

prompt_log = []
# prompt_loc = f"{appdata_location}/prompts.txt"
prompt_loc = f"{appdata_location}/prompts.json"

MAX_TOKENS = 2048
MAX_TEMP = 2


def startup():
    con.print(
        """
 ██████ ██   ██  █████  ████████  ██████ ██      ██ 
██      ██   ██ ██   ██    ██    ██      ██      ██ 
██      ███████ ███████    ██    ██      ██      ██ 
██      ██   ██ ██   ██    ██    ██      ██      ██ 
 ██████ ██   ██ ██   ██    ██     ██████ ███████ ██ 

        written by [link=https://github.com/madstone0-0]madstone0-0[/link]
    """,
        style="green",
    )


help_msgs = {
    "temp": "Controls the randomness of responses,"
    "2 makes output more random, 0 makes it more focused and deterministic",
    "tokens": "Max tokens used",
}


def _version_callback(value: bool) -> None:
    if value:
        con.print(f"v{version('chatcli')}")
        raise typer.Exit()


def load_log(log: str) -> list:
    prompts = []
    try:
        with open(f"{log}", mode="r", encoding="utf-8") as f:
            if f:
                prompts = json.loads(" ".join(f.readlines()))
    except FileNotFoundError:
        return prompts
    return prompts


def get_tokens(prompt: str):
    tokens = word_tokenize(prompt)
    return tokens


def generate_prompt(prompt: str):
    return f"""{prompt}"""


def ask(temp: float, tokens: int, model: str):
    if temp < 0 or temp > MAX_TEMP:
        con.print("[bold red]Temperature cannot be below 0 or above 1[/bold red]")
        raise typer.Exit(1)

    if tokens <= 0 or tokens > MAX_TOKENS:
        con.print("[bold red]Max tokens cannot be below 0 or above 2048[/bold red]")
        raise typer.Exit(1)

    con.print(f"Temperature settings: {temp}\nMax Tokens: {tokens}\nModel: {model}")
    con.print(
        "Enter/Paste your prompt. Ctrl-D or Ctrl-Z on windows to save it. And exit to end the session"
    )

    # https://stackoverflow.com/a/38223253/9784169
    while True:
        prompt_log = load_log(prompt_loc)
        prompt = []
        while True:
            try:
                line = con.input("[green]>[/green] ")
                if line == "exit" or line == "q":
                    con.print("Exiting...")
                    raise typer.Exit()
            except EOFError:
                break
            prompt.append(line)
        prompt = "\n".join(prompt)
        # https://stackoverflow.com/a/38223253/9784169

        # token_num = len(get_tokens(generate_prompt(prompt)))
        try:
            with con.status("Generating"):
                response = openai.Completion.create(
                    model=model,
                    prompt=generate_prompt(prompt),
                    temperature=temp,
                    max_tokens=tokens,
                )

            output = response.choices[0].text
            con.print(f"""\n{output}\n""")
            prompt_log.append({"model": model, "prompt": prompt, "response": output})
            with open(prompt_loc, mode="w", encoding="utf-8") as f:
                json.dump(prompt_log, f, indent=4, ensure_ascii=False)

        except APIConnectionError:
            con.print(
                "Could not connect to API, please check your connection and try again",
                style="red bold",
            )
            continue


def ask_v2(temp: float, tokens: int, model: str, persona: str, is_file: bool | None):

    if temp < 0 or temp > MAX_TEMP:
        con.print("[bold red]Temperature cannot be below 0 or above 1[/bold red]")
        raise typer.Exit(1)

    if tokens <= 0 or tokens > MAX_TOKENS:
        con.print("[bold red]Max tokens cannot be below 0 or above 2048[/bold red]")
        raise typer.Exit(1)

    if is_file:
        with open(persona, "r", encoding="utf-8") as f:
            persona = "".join(f.readlines())

    con.print(f"Temperature settings: {temp}\nMax Tokens: {tokens}\nModel: {model}")
    con.print(f"Current persona settings: {persona}")
    con.print(
        "Enter/Paste your prompt. Ctrl-D or Ctrl-Z on windows to save it. And exit or q to end the session"
    )

    messages = []
    responses = []

    # https://stackoverflow.com/a/38223253/9784169
    while True:
        prompt_log = load_log(prompt_loc)
        prompt = []
        while True:
            try:
                line = con.input("[green]>[/green] ")
                if line == "exit" or line == "q":
                    con.print("Exiting...")
                    raise typer.Exit()
            except EOFError:
                break
            prompt.append(line)
        prompt = "\n".join(prompt)
        # https://stackoverflow.com/a/38223253/9784169

        messages.append({"role": "user", "content": prompt})
        try:
            with con.status("Generating"):
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": persona},
                        *messages,
                        *responses,
                    ],
                )

            output = response["choices"][0]["message"]["content"]
            responses.append({"role": "assistant", "content": output})
            con.print(f"""\n{output}\n""")
            prompt_log.append(
                {
                    "model": model,
                    "persona": persona,
                    "prompt": prompt,
                    "response": output,
                }
            )
            with open(prompt_loc, mode="w", encoding="utf-8") as f:
                json.dump(prompt_log, f, indent=4, ensure_ascii=False)

        except RateLimitError:
            con.print(
                "Current model currently overloaded with requests, please try again later",
                style="red bold",
            )
            # raise typer.Exit(1)
            continue

        except APIConnectionError:
            con.print(
                "Could not connect to API, please check your connection and try again",
                style="red bold",
            )
            continue
            # raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def ask_turbo(
    temp: float = typer.Argument(0.7, help=help_msgs["temp"]),
    tokens: int = typer.Argument(1000, help=help_msgs["tokens"]),
    persona: str = typer.Argument(
        "You are a helpful assistant", help="Assistant persona"
    ),
    is_file: Optional[bool] = typer.Option(
        None, "--file", help="Read persona from file path"
    ),
):
    ask_v2(temp, tokens, model="gpt-3.5-turbo", persona=persona, is_file=is_file)


@app.command()
def ask_davinci_code(
    temp: float = typer.Argument(
        0.7,
        help=help_msgs["temp"],
    ),
    tokens: int = typer.Argument(1000, help=help_msgs["tokens"]),
):
    ask(temp, tokens, model="code-davinci-002")


@app.command()
def ask_davinci_text(
    temp: float = typer.Argument(
        0.7,
        help=help_msgs["temp"],
    ),
    tokens: int = typer.Argument(1000, help=help_msgs["tokens"]),
):
    ask(temp, tokens, model="text-davinci-003")


@app.command()
def ask_davinci(
    temp: float = typer.Argument(
        0.7,
        help=help_msgs["temp"],
    ),
    tokens: int = typer.Argument(1000, help=help_msgs["tokens"]),
):
    ask(temp, tokens, model="davinci")


@app.command()
def ask_ada(
    temp: float = typer.Argument(
        0.7,
        help=help_msgs["temp"],
    ),
    tokens: int = typer.Argument(1000, help=help_msgs["tokens"]),
):
    ask(temp, tokens, model="text-ada-001")


@app.command()
def ask_curie(
    temp: float = typer.Argument(
        0.7,
        help=help_msgs["temp"],
    ),
    tokens: int = typer.Argument(1000, help=help_msgs["tokens"]),
):
    ask(temp, tokens, model="text-curie-001")


@app.command()
def ask_babbage(
    temp: float = typer.Argument(
        0.7,
        help=help_msgs["temp"],
    ),
    tokens: int = typer.Argument(1000, help=help_msgs["tokens"]),
):
    ask(temp, tokens, model="text-babbage-001")


if __name__ == "__main__":
    app()
