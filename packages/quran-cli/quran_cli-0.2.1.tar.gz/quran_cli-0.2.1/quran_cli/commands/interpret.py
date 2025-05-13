"""Interpret command"""

from pathlib import Path
import sqlite3
from typing import Annotated
import typer
from rich import print

from quran_cli import utils


def interpret(
    database: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, help="Database file"),
    ],
    generate_sql: Annotated[
        bool,
        typer.Option(
            "-g",
            "--generate-sql",
            help="Weather to generate SQL statements for this command",
        ),
    ] = False,
) -> None:
    """
    Add Quran interpretations (Al Muyassar) to the database.

    Examples:

    ```bash
    quran-cli init db.sqlite3
    quran-cli normalize -d db.sqlite3
    quran-cli interpret db.sqlite3
    ```
    """

    try:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        print(f"Adding interpretations to [bold]{database}[/bold]...")

        utils.insert_interpretations(cursor, generate_sql)
        utils.insert_trans(cursor, generate_sql)

        connection.commit()
        connection.close()

        print("Interpretation [bold green]completed[/bold green].")

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
