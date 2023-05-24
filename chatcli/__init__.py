from os import getenv, makedirs

from appdirs import user_data_dir
from rich.console import Console

ERROR = "bold red"
EXIT_COMMANDS = ("exit", "q")
ENV = getenv("CHAT_ENV")
appname = "ChatCli"
appauthor = "madstone0-0"
appdata_location = user_data_dir(appname, appauthor)
makedirs(appdata_location, exist_ok=True)


con = Console()
