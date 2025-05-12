import typer

from .getTrades import getTrades

app = typer.Typer()
app.command()(getTrades)


if __name__ == "__main__":
    app()
