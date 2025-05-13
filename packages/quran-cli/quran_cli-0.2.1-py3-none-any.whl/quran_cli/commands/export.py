"""JSON Export command"""

import json
import os
import sqlite3
from pathlib import Path
from typing import Annotated
import typer
from rich import print

from quran_cli import TABLE_FIELDS


def export(
    database: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, help="Database file"),
    ],
    output: Annotated[
        Path,
        typer.Option(
            "-o",
            "--output",
            file_okay=False,
            dir_okay=True,
            help="Output folder",
        ),
    ] = Path("json"),
) -> None:
    """
    Export Quran data to json.

    Examples:

    ```bash
    # Create initial database
    quran-cli init db.sqlite3

    # Normalize initial database
    quran-cli normalize db.sqlite3

    # Export normalized database
    quran-cli export db.sqlite3
    quran-cli export db.sqlite3 -o data
    ```
    """

    try:
        connection = sqlite3.connect(database)
        os.makedirs(output, exist_ok=True)

        print(f"Exporting [bold]{database}[/bold]:")

        for name, fields in TABLE_FIELDS.items():
            print(f"    - [bold]{name}[/bold] table...", end=" ")

            with open(
                f"{os.path.join(output, name)}.json",
                mode="w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    [
                        {fields[k]: v for k, v in list(enumerate(row))}
                        for row in connection.cursor()
                        .execute(f'SELECT * FROM "{name}"')
                        .fetchall()
                    ],
                    file,
                    indent=2,
                    ensure_ascii=False,
                )

            print("[bold green]Done[/bold green]")

        connection.close()

        print("Export [bold green]completed[/bold green].")

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
