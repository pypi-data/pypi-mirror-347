"""Quran CLI, A tool to generate the most sophisticated Quran data."""

# Constants
TABLE_FIELDS = {
    "chapters": {
        0: "id",
        1: "name",
        2: "order",
        3: "type",
        4: "verse_count",
        5: "page_count",
    },
    "parts": {0: "id", 1: "name", 2: "verse_count", 3: "page_count"},
    "groups": {
        0: "id",
        1: "name",
        2: "verse_count",
        3: "page_count",
        4: "part_id",
    },
    "quarters": {
        0: "id",
        1: "name",
        2: "verse_count",
        3: "page_count",
        4: "group_id",
        5: "part_id",
    },
    "pages": {
        0: "id",
        1: "name",
        2: "verse_count",
        3: "chapter_id",
        4: "group_id",
        5: "part_id",
        6: "quarter_id",
    },
    "verses": {
        0: "id",
        1: "number",
        2: "content",
        3: "chapter_id",
        4: "group_id",
        5: "page_id",
        6: "part_id",
        7: "quarter_id",
    },
    "languages": {0: "id", 1: "name", 2: "code"},
    "collections": {
        0: "id",
        1: "type",
        2: "name",
        3: "description",
        4: "language_id",
    },
    "items": {
        0: "id",
        1: "content",
        2: "chapter_id",
        3: "collection_id",
        4: "verse_id",
    },
}
