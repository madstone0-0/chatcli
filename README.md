# ChatCLI

A CLI implementation of Open AI's Chat-GPT. Supports the following models:

- `text-babbage-001`
- `text-curie-001`
- `text-ada-001`
- `davinci`
- `text-davinci-003`
- `code-davinci-002`
- `gpt-3.5-turbo`

## Requirements

- Python 3.10+
- OpenAI API key supplied as the environment variable `OPENAI_API_KEY`

## Building

### Required

- Poetry

```
git clone https://github.com/madstone0-0/chatcli.git
cd chatcli
poetry install
poetry build
```

## Usage

`chatcli <MODEL NAME> <TEMPERATURE> <MAX TOKENS> --<EXTRA ARGS>`

Run `chatcli --help` for all available options

## Prompts

Previous prompts are stored in:

Linux

```
~/.local/share/ChatCli/prompts.json
```

Windows

```
C:\Users\username\AppData\Local\madstone0-0\ChatCli\prompts.json
```

Mac OS

```
/Users/username/Library/Application Support/ChatCli
```
