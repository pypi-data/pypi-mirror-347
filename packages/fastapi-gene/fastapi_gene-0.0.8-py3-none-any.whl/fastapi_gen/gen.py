from typing import Optional

import typer
from rich import print as colored_print
from rich.console import Console
from typing_extensions import Annotated

from fastapi_gen.core import CommandUtility
from fastapi_gen.core._create_model import create_model
from fastapi_gen.core.migration import migrations_and_migrate
from fastapi_gen.utils.enum import MigrationGrade

from . import __version__

console = Console()

app = typer.Typer(rich_markup_mode="rich")


def version_callback(value: bool) -> None:
    if value:
        colored_print(
            f"FastAPI-Gene aka: [blue]FASTAPI GENERATOR[/blue] version: [green]{__version__}[/green]"
        )
        raise typer.Exit()


@app.callback()
def callback(
    version: Annotated[
        Optional[bool],
        typer.Option("--version", help="Show the version", callback=version_callback),
    ] = None,
) -> None:
    """
    FastAPI GENE - The [bold]fastapi[/bold] command line app. 😎
    """
    ...


@app.command()
def createproject(
    project_name: Annotated[str, typer.Argument(help="The name of the Project")],
    target: Annotated[
        Optional[str], typer.Argument(help="Target directory to create Project")
    ] = None,
) -> None:
    """Create a new project scaffold."""
    CommandUtility(project_name, target).execute()


@app.command()
def createuser(
    model: Annotated[str, typer.Argument(help="The name of the Model")],
    target: Annotated[
        Optional[str], typer.Option(help="Target directory to create user table")
    ] = None,
    default: Annotated[
        bool,
        typer.Option(
            help="Set default to create db,schema,app,models files from provided model)"
        ),
    ] = False,
) -> None:
    """
    Create a user table from fastapi-users packages

    [bold green]Supported Models are[/bold green]:

        - [blue]"fastapi-users[yellow][[/yellow]sqlalchemy[yellow]][/yellow]"[/blue]
        - [blue]"fastapi-users[yellow][[/yellow]sqlalchemy,oauth[yellow]][/yellow]"[/blue]
        - [blue]"fastapi-users[yellow][[/yellow]beanie[yellow]][/yellow]"[/blue]
        - [blue]"fastapi-users[yellow][[/yellow]beanie,oauth[yellow]][/yellow]"[/blue]
    """
    create_model(model, target, default)


@app.command()
def makemigrations(
    action: Annotated[
        Optional[str],
        typer.Argument(help="Use 'init' to initialize migrations"),
    ] = None,
    name: Annotated[
        str, typer.Option("--name", help="The name of the migration directory")
    ] = "alembic",
    autogenerate: Annotated[bool, typer.Option(help="Autogenerate migrations")] = True,
    message: Annotated[
        Optional[str], typer.Option("--message", "-m", help="Migration message")
    ] = None,
) -> None:
    """
    Manage Alembic migration setup and generation.

    Examples:
    - Initialize directory: `makemigrations init --name="migrations"`
    - Basic migration: `makemigrations -m "create tables" or --message="create tables"`
    - With no autogenerate: `makemigrations  --no-autogenerate -m "create tables"`
    """
    init = action and action.lower() == "init"
    if init:
        user_input = console.input(
            f"Are you sure you want to create '{name}' directory? [Yes/No]: "
        )
        if user_input.strip().lower() != "yes":
            raise typer.Abort()
    migrations_and_migrate(init, name, autogenerate, message, command="makemigrations")


@app.command()
def migrate(
    action: Annotated[
        MigrationGrade,
        typer.Argument(help="Choose between 'up' or 'down' for upgrade and downgrade"),
    ],
    revision: Annotated[
        Optional[str],
        typer.Argument(
            help="Target revision (e.g., head, base, or a revision ID)",
            rich_help_panel="Revision",
        ),
    ] = None,
) -> None:
    """
    Apply or reverse Alembic migrations.
    """
    migrations_and_migrate(action.value, revision, command="migrate")


def main() -> None:
    app()
