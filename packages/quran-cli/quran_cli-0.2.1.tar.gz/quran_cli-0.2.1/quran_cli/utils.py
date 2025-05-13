"""Utility functions"""

import json
import os
from pathlib import Path
import shutil
import sqlite3
from typing import List, Literal, Optional, Tuple
from rich import print


# Constants
PARENT = Path(__file__).parent
INITIAL_SCHEMA = PARENT / "assets/schemas/initial.sql"


def get_database_name(src: Path) -> str:
    """
    Returns the database name.

    Args:
        src (Path): Database file path

    Returns:
        str: Database name
    """

    return src.name if src.name.endswith((".sqlite3", ".db")) else src.name + ".sqlite3"


def execute_sql_script(database: sqlite3.Cursor, script: str) -> None:
    """
    Executes a SQL script.

    Args:
        database (sqlite3.Cursor): Database cursor
        script (str): SQL script string
    """

    database.executescript(script)


def execute_sql_file(database: sqlite3.Cursor, path: Path) -> None:
    """
    Executes a SQL file.

    Args:
        database (sqlite3.Cursor): Database cursor
        file (str): SQL script filename
    """

    with open(path, "r", encoding="utf-8") as file:
        execute_sql_script(database, file.read())


def apply_initial_schema(database: sqlite3.Cursor, generate_sql: bool = False) -> None:
    """
    Creates the initial schema to insert Quran text.

    Args:
        database (sqlite3.Cursor): Database cursor
        generate_sql (bool): Weather to generate SQL statements
    """

    if generate_sql:
        os.makedirs("sql/workflow", exist_ok=True)
        shutil.copyfile(INITIAL_SCHEMA, "sql/workflow/01-initial-schema.sql")

    print("Creating [bold]the initial schema[/bold]...", end=" ")
    execute_sql_file(database, INITIAL_SCHEMA)
    print("[bold green]Done[/bold green]")


def create_views(database: sqlite3.Cursor, generate_sql: bool = False) -> None:
    """
    Creates views to help with data access.

    Args:
        database (sqlite3.Cursor): Database cursor
        generate_sql (bool): Weather to generate SQL statements
    """

    views = PARENT / "assets/schemas/views.sql"

    if generate_sql:
        shutil.copyfile(views, "sql/workflow/11-views.sql")

    print("Creating [bold]the views[/bold]...", end=" ")
    execute_sql_file(database, views)
    print("[bold green]Done[/bold green]")


def insert_initial_data(database: sqlite3.Cursor, generate_sql: bool = False) -> None:
    """
    Inserts the Quran text into the database

    Args:
        database (sqlite3.Cursor): Database cursor
        generate_sql (bool): Weather to generate SQL statements
    """

    initial_data = PARENT / "assets/data/initial.sql"

    if generate_sql:
        shutil.copyfile(initial_data, "sql/workflow/02-initial-data.sql")

    print("Inserting [bold]initial data[/bold]...", end=" ")
    execute_sql_file(database, initial_data)
    print("[bold green]Done[/bold green]")


def apply_normalized_schema(
    database: sqlite3.Cursor, generate_sql: bool = False
) -> None:
    """
    Creates the normalized schema to normalize the initial database.

    Args:
        database (sqlite3.Cursor): Database cursor
        generate_sql (bool): Weather to generate SQL statements
    """

    schema = PARENT / "assets/schemas/normalized.sql"

    if generate_sql:
        os.makedirs("sql/workflow", exist_ok=True)
        shutil.copyfile(schema, "sql/workflow/03-normalized-schema.sql")

    print("Creating [bold]the normalized schema[/bold]...", end=" ")
    execute_sql_file(database, schema)
    print("[bold green]Done[/bold green]")


def insert_chapters(
    database: sqlite3.Cursor,
    with_diacritics: bool = False,
    generate_sql: bool = False,
) -> None:
    """
    Insert chapters (Al-Suwar) data into the database.

    Args:
        database (sqlite3.Cursor): Database cursor
        with_diacritics (bool): Weather to include arabic diacritics in chapter names
        generate_sql (bool): Weather to generate SQL statements
    """

    chapters = PARENT / "assets/data/chapters.sql"

    if generate_sql:
        shutil.copyfile(chapters, "sql/workflow/04-chapters.sql")

    print("Inserting [bold]chapters[/bold]...", end=" ")
    execute_sql_file(database, chapters)

    if with_diacritics:
        src = PARENT / "assets/data/chapters.json"

        with open(src, encoding="utf-8") as f:
            statements = "".join(
                [
                    f'UPDATE "chapters" SET "name" = "{chapter['new_name']}" WHERE "id" = {chapter['id']};\n'
                    for chapter in json.load(f)
                ]
            )

            if generate_sql:
                with open(
                    "sql/workflow/04-chapters.sql", "a", encoding="utf-8"
                ) as output:
                    output.write("\n\n" + statements)

            execute_sql_script(database, statements)

    print("[bold green]Done[/bold green]")


def get_verse(
    database: sqlite3.Cursor,
    chapter_id: int,
    verse_number: int,
) -> Tuple[int, int, int, str]:
    """
    Get a verse by chapter id and verse number.

    Args:
        database (sqlite3.Cursor): Database cursor
        chapter_id (int): Chapter ID
        verse_number (int): Verse number

    Returns:
        Tuple[int, int, int, str]: Tuple with the verse data
    """

    return database.execute(
        "SELECT * FROM quran WHERE chapter_id = ? AND number = ?",
        (chapter_id, verse_number),
    ).fetchone()


def get_verse_range(
    database: sqlite3.Cursor,
    start: Tuple[int, int],
    end: Tuple[int, int],
) -> Tuple[int, int]:
    """
    Get the verse range as (start_verse_id, end_verse_id).

    Args:
        database (sqlite3.Cursor): Database cursor
        start (Tuple[int, int]): Start chapter_id and verse_number
        end (Tuple[int, int]): End chapter_id and verse_number

    Returns:
        Tuple[int, int]: Tuple with the start and end verse ids
    """

    return (
        get_verse(database, start[0], start[1])[0],
        get_verse(database, end[0], end[1])[0] - 1,
    )


def get_table_verse_range(
    database: sqlite3.Cursor,
    table: Literal["parts", "pages", "quarters"],
) -> List[Tuple[int, int]]:
    """
    Get verse ranges for each part, quarter and page as (start_verse_id, end_verse_id).
    The index of the item in the returned list represents the id of the part, quarter or page.

    Args:
        database (sqlite3.Cursor): Database cursor
        table (str): Table name

    Returns:
        List[Tuple[int, int]]: Verse range representation of each item in the list.
    """

    with open(
        PARENT / "assets/data/metadata.json",
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)[table]

        res = []
        for index, item in enumerate(data):
            if index < len(data) - 1:
                res.append(get_verse_range(database, item, data[index + 1]))
            else:
                res.append((res[-1][1] + 1, 6236))

        return res


def insert_verses(database: sqlite3.Cursor, generate_sql: bool = False) -> None:
    """
    Insert verses (Al-Aayat) data into the database.

    Args:
        database (sqlite3.Cursor): Database cursor
        generate_sql (bool): Weather to generate SQL statements
    """

    statement = 'INSERT INTO "verses" ("number", "content", "chapter_id") SELECT "number", "content", "chapter_id" FROM "quran";'

    if generate_sql:
        with open("sql/workflow/05-verses.sql", "w", encoding="utf-8") as output:
            output.write(statement)

    print("Inserting [bold]verses[/bold]...", end=" ")
    execute_sql_script(database, statement)
    print("[bold green]Done[/bold green]")


def insert_table_data(database: sqlite3.Cursor, generate_sql: bool = False) -> None:
    """
    Insert data into parts, groups, quarters and pages tables.

    Args:
        database (sqlite3.Cursor): Database cursor
        generate_sql (bool): Weather to generate SQL statements
    """

    statements = "".join(
        [
            *[
                f'INSERT INTO "parts" (name) VALUES ("الجزء {p}");\n'
                for p in range(1, 31)
            ],
            *[
                f'INSERT INTO "groups" (name) VALUES ("الحزب {g}");\n'
                for g in range(1, 61)
            ],
            *[
                f'INSERT INTO "quarters" (name) VALUES ("الربع {q}");\n'
                for q in range(1, 241)
            ],
            *[
                f'INSERT INTO "pages" (name) VALUES ("الصفحة {p}");\n'
                for p in range(1, 605)
            ],
        ]
    )

    if generate_sql:
        with open("sql/workflow/06-tables.sql", "w", encoding="utf-8") as output:
            output.write(statements)

    print(
        "Inserting data into [bold]parts, groups, quarters and pages tables[/bold]...",
        end=" ",
    )
    execute_sql_script(database, statements)
    print("[bold green]Done[/bold green]")


def set_verse_fks(database: sqlite3.Cursor, generate_sql: bool = False) -> None:
    """
    Update the verses table to set part_id, group_id, quarter_id and page_id.

    Args:
        database (sqlite3.Cursor): Database cursor
        generate_sql (bool): Weather to generate SQL statements
    """

    print(
        "Updating [bold]verses[/bold] table to set "
        "[bold]part_id, group_id, quarter_id and page_id[/bold]...",
        end=" ",
    )

    statements = [
        "".join(
            [
                # Generate SQL statement for each range
                f'UPDATE "verses" SET "{t[:-1]}_id" = {id} WHERE "id" BETWEEN {item[0]} AND {item[1]};\n'
                for id, item in enumerate(get_table_verse_range(database, t), start=1)
            ]
        )
        # Generate verse ranges for each table
        for t in ["parts", "quarters", "pages"]
    ]

    # Compute group ranges based on quarter ranges; Group = 4 Quarter
    q_ranges = get_table_verse_range(database, "quarters")
    statements.insert(
        1,
        "".join(
            [
                f'UPDATE "verses" SET group_id = {i} WHERE "id" BETWEEN {g[0]} AND {g[1]};\n'
                for i, g in enumerate(
                    # Compute group ranges
                    [
                        (
                            q_ranges[i][0],
                            q_ranges[i + 3][1] if i + 4 < len(q_ranges) - 1 else 6236,
                        )
                        for i in range(0, 240, 4)
                    ],
                    start=1,
                )
            ]
        ),
    )

    statements = "".join(statements)

    if generate_sql:
        with open("sql/workflow/07-verse-fks.sql", "w", encoding="utf-8") as output:
            output.write(statements)

    execute_sql_script(database, statements)

    print("[bold green]Done[/bold green]")


def set_verse_count(database: sqlite3.Cursor, generate_sql: bool = False) -> None:
    """
    Update corresponding tables to set verse_count.

    Args:
        database (sqlite3.Cursor): Database cursor
        generate_sql (bool): Weather to generate SQL statements
    """

    print("Setting [bold]verse_count[/bold]...", end=" ")

    statements = "".join(
        [
            "".join(
                [
                    # Generate corresponding SQL statement
                    f'UPDATE {t} SET "verse_count" = {item[0]} WHERE "id" = {id};\n'
                    # Compute verse_count for each item in each table with item id
                    for id, item in enumerate(
                        database.execute(
                            f'SELECT COUNT(*) FROM "verses" GROUP BY "{t[:-1]}_id"'
                        ).fetchall(),
                        start=1,
                    )
                ]
            )
            for t in ["parts", "groups", "quarters", "pages"]
        ]
    )

    if generate_sql:
        with open("sql/workflow/08-verse-count.sql", "w", encoding="utf-8") as output:
            output.write(statements)

    execute_sql_script(database, statements)

    print("[bold green]Done[/bold green]")


def set_page_count(database: sqlite3.Cursor, generate_sql: bool = False) -> None:
    """
    Update corresponding tables to set page_count.

    Args:
        database (sqlite3.Cursor): Database cursor
        generate_sql (bool): Weather to generate SQL statements
    """

    print("Setting [bold]page_count[/bold]...", end=" ")

    statements = "".join(
        [
            "".join(
                [
                    f'UPDATE {t} SET "page_count" = {item[0]} WHERE "id" = {id};\n'
                    for id, item in enumerate(
                        database.execute(
                            'SELECT COUNT(DISTINCT "pages"."id") FROM "pages" INNER JOIN "verses" ON '
                            f'("pages"."id" = "verses"."page_id") GROUP BY "verses"."{t[:-1]}_id"'
                        ).fetchall(),
                        start=1,
                    )
                ]
            )
            for t in ["chapters", "parts", "groups", "quarters"]
        ]
    )

    if generate_sql:
        with open("sql/workflow/10-page-count.sql", "w", encoding="utf-8") as output:
            output.write(str(statements))

    execute_sql_script(database, statements)
    print("[bold green]Done[/bold green]")


def set_foreign_keys(database: sqlite3.Cursor, generate_sql: bool = False) -> None:
    """
    Update groups, quarters and pages tables to set foreign keys.

    Args:
        database (sqlite3.Cursor): Database cursor
        generate_sql (bool): Weather to generate SQL statements
    """

    print(
        "Setting foreign keys for [bold]groups, quarters and pages tables[/bold]...",
        end=" ",
    )

    tables = [
        {
            "name": "groups",
            "select": 'SELECT "part_id" FROM "verses" GROUP BY "group_id"',
            "update": 'UPDATE "groups" SET "part_id" = %s WHERE "id" = %s;\n',
        },
        {
            "name": "quarters",
            "select": 'SELECT "part_id", "group_id" FROM "verses" GROUP BY "quarter_id"',
            "update": 'UPDATE "quarters" SET "part_id" = %s, "group_id" = %s WHERE "id" = %s;\n',
        },
        {
            "name": "pages",
            "select": 'SELECT "chapter_id", "part_id", "group_id", "quarter_id" FROM "verses" GROUP BY "page_id"',
            "update": 'UPDATE "pages" SET "chapter_id" = %s, "part_id" = %s, "group_id" = %s, "quarter_id" = %s WHERE "id" = %s;\n',
        },
    ]

    statements = "".join(
        [
            "".join(
                [
                    t["update"] % (*item, id)
                    for id, item in enumerate(
                        database.execute(t["select"]).fetchall(), start=1
                    )
                ]
            )
            for t in tables
        ]
    )

    if generate_sql:
        with open("sql/workflow/09-tables_fks.sql", "w", encoding="utf-8") as output:
            output.write(statements)

    execute_sql_script(database, statements)

    print("[bold green]Done[/bold green]")


def insert_items(
    database: sqlite3.Cursor,
    collection_id: int,
    generate_sql: bool = False,
    file_name: Optional[str] = None,
) -> None:
    """
    Insert items data into the database.

    Args:
        database (sqlite3.Cursor): Database cursor
        collection_id (int): Collection ID
        generate_sql (bool): Weather to generate SQL statements
        file_name (str): File name to write if generate_sql is true
    """

    statement = f'INSERT INTO "items"("content", "collection_id", "verse_id") SELECT "content", {collection_id}, "id" FROM "quran"'

    if generate_sql and file_name:
        with open(f"sql/workflow/{file_name}.sql", "a", encoding="utf-8") as output:
            output.write(statement)

    print("Inserting [bold]items[/bold]...", end=" ")
    execute_sql_script(database, statement)
    print("[bold green]Done[/bold green]")


def insert_interpretations(
    database: sqlite3.Cursor, generate_sql: bool = False
) -> None:
    """
    Insert interpretations (Tafsir) data into the database.

    Args:
        database (sqlite3.Cursor): Database cursor
        generate_sql (bool): Weather to generate SQL statements
    """

    initial_data = PARENT / "assets/data/interpretations.sql"
    schema = PARENT / "assets/schemas/comp.sql"
    data = PARENT / "assets/data/comp.sql"

    if generate_sql:
        os.makedirs("sql/workflow", exist_ok=True)
        shutil.copyfile(INITIAL_SCHEMA, "sql/workflow/12-initial-schema.sql")
        shutil.copyfile(initial_data, "sql/workflow/13-interpretations-initial.sql")
        shutil.copyfile(schema, "sql/workflow/14-comp-schema.sql")
        shutil.copyfile(data, "sql/workflow/15-comp-data.sql")

    print("Inserting [bold]interpretations[/bold]...")
    apply_initial_schema(database)
    execute_sql_file(database, initial_data)
    execute_sql_file(database, schema)
    execute_sql_file(database, data)
    insert_items(database, 1, generate_sql, "16-interpretations")


def insert_trans(database: sqlite3.Cursor, generate_sql: bool = False) -> None:
    """
    Insert translation and transliteration data into database.

    Args:
        database (sqlite3.Cursor): Database cursor
        generate_sql (bool): Weather to generate SQL statements
    """

    translations = PARENT / "assets/data/translations.sql"
    transliterations = PARENT / "assets/data/transliterations.sql"

    if generate_sql:
        shutil.copyfile(INITIAL_SCHEMA, "sql/workflow/17-initial-schema.sql")
        shutil.copyfile(translations, "sql/workflow/18-translations-initial.sql")
        shutil.copyfile(INITIAL_SCHEMA, "sql/workflow/20-initial-schema.sql")
        shutil.copyfile(
            transliterations, "sql/workflow/21-transliterations-initial.sql"
        )

    print("Inserting [bold]trans[/bold]...")
    apply_initial_schema(database)
    execute_sql_file(database, translations)
    insert_items(database, 2, generate_sql, "19-translations")
    apply_initial_schema(database)
    execute_sql_file(database, transliterations)
    insert_items(database, 3, generate_sql, "22-transliterations")
