from importlib.metadata import version
from typing import Optional

import typer

from chatcli import con
from chatcli.ask import Ask
from chatcli.model import Model

app = typer.Typer()
ask = Ask()

help_msgs = {
    "temp": "Controls the randomness of responses,"
    "2 makes output more random, 0 makes it more focused and deterministic",
    "tokens": "Max tokens used",
}

gpt4_models = {
    "default": Model(name="gpt-4", nickname="gpt4", maxTokens=8192),
    "32k": Model(name="gpt-4-32k", nickname="gpt4-32k", maxTokens=32768),
    "turbo": Model(name="gpt-4-1106-preview", nickname="gpt4-turbo", maxTokens=128000),
}

gpt3_5_models = {
    "default": Model(name="gpt-3.5-turbo", nickname="gpt3", maxTokens=4096),
    "16k": Model(name="gpt-3.5-16k", nickname="gpt3-16k", maxTokens=16385),
}

opts = {
    "temp": typer.Argument(0.7, help=help_msgs["temp"]),
    "tokens": typer.Argument(1000, help=help_msgs["tokens"]),
    "persona": typer.Argument("You are a helpful assistant", help="Assistant persona"),
    "is_file": typer.Option(None, "--file", help="Read persona from file path"),
    "json_mode": typer.Option(False, "--json", help="Enable JSON mode"),
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
    ),
) -> None:
    return


@app.command()
def ask_gpt4_turbo(
    temp: float = opts["temp"],
    tokens: int = opts["tokens"],
    persona: str = opts["persona"],
    is_file: Optional[bool] = opts["is_file"],
    json_mode: Optional[bool] = opts["json_mode"],
):
    ask.ask(
        temp,
        tokens,
        model=gpt4_models["turbo"],
        persona=persona,
        is_file=is_file,
        json_mode=json_mode,
    )


@app.command()
def ask_gpt4(
    temp: float = opts["temp"],
    tokens: int = opts["tokens"],
    persona: str = opts["persona"],
    is_file: Optional[bool] = opts["is_file"],
    json_mode: Optional[bool] = opts["json_mode"],
):
    ask.ask(
        temp,
        tokens,
        model=gpt4_models["default"],
        persona=persona,
        is_file=is_file,
        json_mode=json_mode,
    )


@app.command()
def ask_gpt4_32k(
    temp: float = opts["temp"],
    tokens: int = opts["tokens"],
    persona: str = opts["persona"],
    is_file: Optional[bool] = opts["is_file"],
    json_mode: Optional[bool] = opts["json_mode"],
):
    ask.ask(
        temp,
        tokens,
        model=gpt4_models["32k"],
        persona=persona,
        is_file=is_file,
        json_mode=json_mode,
    )


@app.command()
def ask_turbo(
    temp: float = opts["temp"],
    tokens: int = opts["tokens"],
    persona: str = opts["persona"],
    is_file: Optional[bool] = opts["is_file"],
    json_mode: Optional[bool] = opts["json_mode"],
):
    ask.ask(
        temp,
        tokens,
        model=gpt3_5_models["default"],
        persona=persona,
        is_file=is_file,
        json_mode=json_mode,
    )


@app.command()
def ask_turbo_16k(
    temp: float = opts["temp"],
    tokens: int = opts["tokens"],
    persona: str = opts["persona"],
    is_file: Optional[bool] = opts["is_file"],
    json_mode: Optional[bool] = opts["json_mode"],
):
    ask.ask(
        temp,
        tokens,
        model=gpt3_5_models["16k"],
        persona=persona,
        is_file=is_file,
        json_mode=json_mode,
    )
