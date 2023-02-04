#!/usr/bin/python3.11
import os

import openai
import typer
from rich.console import Console
from appdirs import user_data_dir
from transformers import GPT2TokenizerFast

appname = "ChatCli"
appauthor = "madstone0-0"
appdata_location = user_data_dir(appname, appauthor)
os.makedirs(appdata_location, exist_ok=True)

openai.api_key = os.getenv("OPENAI_API_KEY")
app = typer.Typer()
con = Console()

prompt_loc = f"{appdata_location}/prompts.txt"


def generate_prompt(prompt: str):
    return f"""{prompt}"""


def ask(temp: float, tokens: int, model: str):
    if temp < 0 or temp > 1:
        con.print("[bold red]Temperature cannot be below 0 or above 1[/bold red]")
        raise typer.Exit(1)

    if tokens <= 0 or tokens > 2048:
        con.print("[bold red]Max tokens cannot be below 0 or above 2048[/bold red]")
        raise typer.Exit(1)

    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    prompt = typer.prompt("Enter prompt")
    prompt_tokens = tokenizer(generate_prompt(prompt))
    token_num = len(prompt_tokens["input_ids"])
    with con.status("Generating"):
        response = openai.Completion.create(
            model=model,
            prompt=generate_prompt(prompt),
            temperature=temp,
            max_tokens=int(tokens - token_num),
        )
    con.print(f"""{response.choices[0].text}""")
    with open(prompt_loc, mode="a+", encoding="utf-8") as f:
        response = response.choices[0].text
        f.write(f"Model: {model}\nPrompt: {prompt}\nResponse: {response}\n\n")


@app.command()
def ask_davinci_text(
    temp: float = typer.Argument(0.7), tokens: int = typer.Argument(1000)
):
    ask(temp, tokens, model="text-davinci-003")


@app.command()
def ask_davinci(temp: float = typer.Argument(0.7), tokens: int = typer.Argument(1000)):
    ask(temp, tokens, model="davinci")


@app.command()
def ask_ada(temp: float = typer.Argument(0.7), tokens: int = typer.Argument(1000)):
    ask(temp, tokens, model="text-ada-001")


@app.command()
def ask_curie(temp: float = typer.Argument(0.7), tokens: int = typer.Argument(1000)):
    ask(temp, tokens, model="text-curie-001")


@app.command()
def ask_babbage(temp: float = typer.Argument(0.7), tokens: int = typer.Argument(1000)):
    ask(temp, tokens, model="text-babbage-001")


if __name__ == "__main__":
    app()
