"""Normalize command"""

from pathlib import Path
import sqlite3
from typing import Annotated
import typer
from rich import print

from quran_cli import utils


def normalize(
    database: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, help="Database file"),
    ],
    diacritics: Annotated[
        bool,
        typer.Option(
            "-d",
            "--with-diacritics",
            help="Weather to include Arabic diacritics in chapter names",
        ),
    ] = False,
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
    Normalize initial Quran database.

    Examples:

    ```bash
    # Create initial database
    quran-cli init db.sqlite3

    quran-cli normalize db.sqlite3
    ```
    """

    try:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()

        print(f"Normalizing [bold]{database}[/bold]...")

        utils.apply_normalized_schema(cursor, generate_sql)
        utils.insert_chapters(cursor, diacritics, generate_sql)
        utils.insert_verses(cursor, generate_sql)
        utils.insert_table_data(cursor, generate_sql)
        utils.set_verse_fks(cursor, generate_sql)
        utils.set_verse_count(cursor, generate_sql)
        utils.set_foreign_keys(cursor, generate_sql)
        utils.set_page_count(cursor, generate_sql)
        utils.create_views(cursor, generate_sql)

        connection.commit()
        connection.close()

        print("Normalization [bold green]completed[/bold green].")

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
