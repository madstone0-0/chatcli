import json

from nltk.tokenize import word_tokenize


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
