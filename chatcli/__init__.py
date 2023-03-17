import os

from appdirs import user_data_dir
from rich.console import Console

appname = "ChatCli"
appauthor = "madstone0-0"
appdata_location = user_data_dir(appname, appauthor)
os.makedirs(appdata_location, exist_ok=True)


con = Console()
