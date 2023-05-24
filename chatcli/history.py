import os.path
from typing import Iterable

from prompt_toolkit.history import History

from chatcli import EXIT_COMMANDS


class PromptHistory(History):
    """Implementation of prompt_toolkit's FileHistory class that doesn't add the time."""

    def __init__(self, filename: str):
        self.filename = filename
        self.cmds = tuple(f"+{cmd}" for cmd in EXIT_COMMANDS)
        super().__init__()

    def load_history_strings(self) -> Iterable[str]:
        strings: list[str] = []
        lines: list[str] = []

        def add() -> None:
            if lines:
                strings.append("".join(lines))
                lines.clear()

        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                for line in f:
                    if line.strip("\n") in self.cmds:
                        continue
                    if line.startswith("+"):
                        lines.append(line[1:])
                    else:
                        add()
                        lines = []

                add()
        return reversed(strings)

    def store_string(self, string: str) -> None:
        with open(self.filename, "ab") as f:
            f.write("\n".encode("utf-8"))
            for line in string.split("\n"):
                if line.strip("\n") in self.cmds:
                    continue
                f.write(f"+{line}\n".encode("utf-8"))
