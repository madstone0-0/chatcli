from importlib.metadata import version
from typing import Optional

import typer

from chatcli import con
from chatcli.ask import Ask

app = typer.Typer()
ask = Ask()

help_msgs = {
    "temp": "Controls the randomness of responses,"
    "2 makes output more random, 0 makes it more focused and deterministic",
    "tokens": "Max tokens used",
}

gpt4_models = {"default": "gpt-4", "32k": "gpt-4-32k", "turbo": "gpt-4-1106-preview"}

gpt3_5_models = {"default": "gpt-3.5-turbo", "16k": "gpt-3.5-turbo-16k"}


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
def ask_gpt4_turbo(
temp: float = typer.Argument(0.7, help=help_msgs["temp"]),
    tokens: int = typer.Argument(1000, help=help_msgs["tokens"]),
    persona: str = typer.Argument("You are a helpful assistant", help="Assistant persona"),
    is_file: Optional[bool] = typer.Option(None, "--file", help="Read persona from file path"),
):
    ask.ask(temp, tokens, model=gpt4_models["turbo"], persona=persona, is_file=is_file)


@app.command()
def ask_gpt4(
    temp: float = typer.Argument(0.7, help=help_msgs["temp"]),
    tokens: int = typer.Argument(1000, help=help_msgs["tokens"]),
    persona: str = typer.Argument("You are a helpful assistant", help="Assistant persona"),
    is_file: Optional[bool] = typer.Option(None, "--file", help="Read persona from file path"),
):
    ask.ask(temp, tokens, model=gpt4_models["default"], persona=persona, is_file=is_file)


@app.command()
def ask_gpt4_32k(
    temp: float = typer.Argument(0.7, help=help_msgs["temp"]),
    tokens: int = typer.Argument(1000, help=help_msgs["tokens"]),
    persona: str = typer.Argument("You are a helpful assistant", help="Assistant persona"),
    is_file: Optional[bool] = typer.Option(None, "--file", help="Read persona from file path"),
):
    ask.ask(temp, tokens, model=gpt4_models["32k"], persona=persona, is_file=is_file)


@app.command()
def ask_turbo(
    temp: float = typer.Argument(0.7, help=help_msgs["temp"]),
    tokens: int = typer.Argument(1000, help=help_msgs["tokens"]),
    persona: str = typer.Argument("You are a helpful assistant", help="Assistant persona"),
    is_file: Optional[bool] = typer.Option(None, "--file", help="Read persona from file path"),
):
    ask.ask(temp, tokens, model=gpt3_5_models["default"], persona=persona, is_file=is_file)


@app.command()
def ask_turbo_16k(
    temp: float = typer.Argument(0.7, help=help_msgs["temp"]),
    tokens: int = typer.Argument(1000, help=help_msgs["tokens"]),
    persona: str = typer.Argument("You are a helpful assistant", help="Assistant persona"),
    is_file: Optional[bool] = typer.Option(None, "--file", help="Read persona from file path"),
):
    ask.ask(temp, tokens, model=gpt3_5_models["16k"], persona=persona, is_file=is_file)
