from chatcli import appname
from chatcli.cli import app


def main():
    app(prog_name=appname.lower())


if __name__ == "__main__":
    main()
