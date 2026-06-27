from runtime.bootstrap import bootstrap
from launcher.console import start_console


def main():
    """
    Application entry point.
    """

    runner, session = bootstrap()

    start_console(
        runner,
        session,
    )


if __name__ == "__main__":
    main()