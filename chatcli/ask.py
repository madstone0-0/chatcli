import json
import os

import openai
import typer
# from icecream import ic
from openai.error import APIConnectionError, RateLimitError
from prompt_toolkit import PromptSession

from chatcli import appdata_location, con
from chatcli.history import PromptHistory
from chatcli.utils import generate_prompt, load_log, read_prompt

MAX_TOKENS = 2048
MAX_TEMP = 2

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt_loc = f"{appdata_location}/prompts_test.json"


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


class Ask:
    def __init__(self):
        self.prompt_log = load_log(prompt_loc)
        self.session = PromptSession(
            history=PromptHistory(f"{appdata_location}/prompt_history")
        )

    def ask_v1(self, temp: float, tokens: int, model: str):
        if temp < 0 or temp > MAX_TEMP:
            con.print("[bold red]Temperature cannot be below 0 or above 1[/bold red]")
            raise typer.Exit(1)

        if tokens <= 0 or tokens > MAX_TOKENS:
            con.print("[bold red]Max tokens cannot be below 0 or above 2048[/bold red]")
            raise typer.Exit(1)

        startup()

        con.print(f"Temperature settings: {temp}\nMax Tokens: {tokens}\nModel: {model}")
        con.print(
            "Enter/Paste your prompt. Esc-Enter save it and exit or q to end the session"
        )

        while True:
            self.prompt_log = load_log(prompt_loc)
            prompt = read_prompt(self.session)

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
                self.prompt_log.append(
                    {"model": model, "prompt": prompt, "response": output}
                )
                with open(prompt_loc, mode="w", encoding="utf-8") as f:
                    json.dump(self.prompt_log, f, indent=4, ensure_ascii=False)

            except APIConnectionError:
                con.print(
                    "Could not connect to API, please check your connection and try again",
                    style="red bold",
                )
                continue

    def ask_v2(
        self, temp: float, tokens: int, model: str, persona: str, is_file: bool | None
    ):
        if temp < 0 or temp > MAX_TEMP:
            con.print("[bold red]Temperature cannot be below 0 or above 1[/bold red]")
            raise typer.Exit(1)

        if tokens <= 0 or tokens > MAX_TOKENS:
            con.print("[bold red]Max tokens cannot be below 0 or above 2048[/bold red]")
            raise typer.Exit(1)

        if is_file:
            with open(persona, "r", encoding="utf-8") as f:
                persona = "".join(f.readlines())

        startup()

        con.print(f"Temperature settings: {temp}\nMax Tokens: {tokens}\nModel: {model}")
        con.print(f"Current persona settings: {persona}")
        con.print(
            "Enter/Paste your prompt. Esc-Enter save it and exit or q to end the session"
        )

        messages = []
        responses = []

        # https://stackoverflow.com/a/38223253/9784169
        while True:
            self.prompt_log = load_log(prompt_loc)
            prompt = read_prompt(self.session)

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
                self.prompt_log.append(
                    {
                        "model": model,
                        "persona": persona,
                        "prompt": prompt,
                        "response": output,
                    }
                )
                with open(prompt_loc, mode="w", encoding="utf-8") as f:
                    json.dump(self.prompt_log, f, indent=4, ensure_ascii=False)

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
