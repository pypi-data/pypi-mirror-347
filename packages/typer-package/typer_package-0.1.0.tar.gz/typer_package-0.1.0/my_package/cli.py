import typer
from my_package.utils import say_hello  # 👈 import from another file

app = typer.Typer()

@app.command()
def hello():
    """Prints a simple hello."""
    typer.echo("Hello, world!")

@app.command()
def greet(name: str):
    """Greets a person using the say_hello utility function."""
    typer.echo(say_hello(name))
