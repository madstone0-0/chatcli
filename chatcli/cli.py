#!/usr/bin/python3.11
from importlib.metadata import version
from typing import Optional

import typer

from chatcli import con
from chatcli.ask import ask, ask_v2

# from icecream import ic

app = typer.Typer()


help_msgs = {
    "temp": "Controls the randomness of responses,"
    "2 makes output more random, 0 makes it more focused and deterministic",
    "tokens": "Max tokens used",
}


def _version_callback(value: bool) -> None:
    if value:
        con.print(f"v{version('chatcli')}")
        raise typer.Exit()


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
