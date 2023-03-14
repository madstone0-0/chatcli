from chatcli.cli import app, startup


def main():
    startup()
    app(prog_name="chatcli")


if __name__ == "__main__":
    main()
