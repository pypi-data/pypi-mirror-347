import typer

from .getTrades import main_cli_entrypoint

app = typer.Typer()
app.command(main_cli_entrypoint)


if __name__ == "__main__":
    app()
