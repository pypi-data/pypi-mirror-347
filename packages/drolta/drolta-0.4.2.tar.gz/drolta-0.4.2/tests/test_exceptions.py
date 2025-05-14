"""Drolta tests for proper exception raising."""

import sqlite3

import pytest
from drolta import QueryEngine
from drolta.errors import ProgrammingError


def initialize_test_data(db: sqlite3.Connection) -> None:
    """Initializes the provided data"""

    cursor = db.cursor()

    cursor.executescript(
        """
        DROP TABLE IF EXISTS characters;
        DROP TABLE IF EXISTS houses;
        DROP TABLE IF EXISTS relations;

        CREATE TABLE characters (
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT,
            house_id INTEGER,
            sex TEXT,
            life_stage TEXT,
            is_alive INTEGER,
            FOREIGN KEY (house_id) REFERENCES houses(id)
        ) STRICT;

        CREATE TABLE houses (
            id INTEGER NOT NULL PRIMARY KEY,
            name TEXT NOT NULL,
            reputation INT NOT NULL,
            is_noble INT NOT NULL
        ) STRICT;

        CREATE TABLE relations (
            from_id INTEGER NOT NULL,
            to_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            FOREIGN KEY (from_id) REFERENCES characters(id),
            FOREIGN KEY (to_id) REFERENCES characters(id)
        ) STRICT;
        """
    )

    cursor.executemany(
        """
        INSERT INTO
        characters (id, name, house_id, sex, life_stage, is_alive)
        VALUES
        (?, ?, ?, ?, ?, ?);
        """,
        [
            (1, "Rhaenyra", 1, "F", "Adult", 1),
            (2, "Laenor", 2, "M", "Adult", 1),
            (3, "Harwin", 3, "M", "Adult", 1),
            (4, "Jacaerys", 2, "M", "Teen", 1),
            (5, "Addam", None, "M", "Teen", 1),
            (6, "Corlys", 2, "M", "Adult", 1),
            (7, "Marilda", None, "F", "Adult", 0),
            (8, "Alyn", None, "M", "Adult", 1),
            (9, "Rhaenys", 1, "F", "Adult", 0),
            (10, "Laena", 2, "F", "Adult", 0),
            (11, "Daemon", 1, "M", "Adult", 1),
            (12, "Baela", 1, "F", "Teen", 1),
            (13, "Viserys", 1, "M", "Senior", 0),
            (14, "Alicent", 5, "F", "Adult", 1),
            (15, "Otto", 5, "M", "Senior", 1),
            (16, "Aegon", 1, "M", "Teen", 1),
            (17, "Cristen", 4, "M", "Adult", 1),
        ],
    )

    cursor.executemany(
        """
        INSERT INTO
            houses(id, name, reputation, is_noble)
        VALUES
            (?, ?, ?, ?);
        """,
        [
            (1, "Targaryen", 85, 1),
            (2, "Velaryon", 80, 1),
            (3, "Strong", 20, 0),
            (4, "Cole", -20, 0),
            (5, "Hightower", 50, 1),
        ],
    )

    cursor.executemany(
        """
        INSERT INTO
            relations (from_id, to_id, type)
        VALUES
            (?, ?, ?);
        """,
        [
            (4, 1, "Mother"),  # Jace -> Rhaenyra
            (4, 2, "Father"),  # Jace -> Laenor
            (4, 3, "BiologicalFather"),  # Jace -> Harwin
            (5, 6, "BiologicalFather"),  # Addam -> Corlys
            (2, 6, "BiologicalFather"),  # Laenor -> Corlys
            (2, 6, "Father"),  # Laenor -> Corlys
            (5, 7, "Mother"),  # Addam -> Marilda
            (8, 7, "Mother"),  # Alyn -> Marilda
            (8, 6, "BiologicalFather"),  # Alyn -> Corlys
            (2, 9, "Mother"),  # Laenor -> Rhaenys
            (10, 9, "Mother"),  # Laena -> Rhaenys
            (10, 6, "Father"),  # Laena -> Corlys
            (10, 6, "BiologicalFather"),  # Laena -> Corlys
            (6, 9, "Widower"),  # Corlys -> Rhaenys
            (6, 9, "FormerSpouse"),  # Corlys -> Rhaenys
            (9, 6, "FormerSpouse"),  # Rhaenys -> Corlys
            (12, 10, "Mother"),  # Baela -> Laena
            (12, 11, "Father"),  # Baela -> Daemon
            (12, 11, "BiologicalFather"),  # Baela -> Daemon
            (1, 11, "Spouse"),  # Rhaenyra -> Daemon
            (11, 1, "Spouse"),  # Daemon -> Rhaenyra
            (10, 11, "FormerSpouse"),  # Laena -> Daemon
            (11, 10, "FormerSpouse"),  # Daemon -> Laena
            (11, 10, "Widower"),  # Daemon -> Laena
            (1, 13, "Father"),  # Rhaenyra -> Viserys
            (1, 13, "BiologicalFather"),  # Rhaenyra -> Viserys
            (16, 14, "Mother"),  # Aegon -> Alicent
            (14, 15, "Father"),  # Alicent => Otto
            (14, 15, "BiologicalFather"),  # Alicent => Otto
        ],
    )

    db.commit()


def test_unused_output_variable() -> None:
    """Ensure exception is thrown if an output variable is unused.

    This means that the variable appears within the FIND/DEFINE clause but is not
    used within the WHERE clause of a query/rule. Without this exception, the user
    would see a sqlite3.OperationalError for 'no such column: <variable name>'.
    """

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = QueryEngine()

    with pytest.raises(
        ProgrammingError,
        match=r"Parameter \?house_id does not appear in WHERE section of the query.",
    ):
        engine.query(
            """
            FIND
                ?character_id, ?house_id
            WHERE
                characters(id=?character_id);
            """,
            db,
        ).fetch_all()


def test_invalid_predicate_parameter() -> None:
    """Ensure exception is thrown if a predicate parameter is misspelled or invalid."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = QueryEngine()

    with pytest.raises(
        ProgrammingError,
        match=r"character_id is not a valid parameter of predicate characters.",
    ):
        engine.query(
            """
            FIND
                ?character_id
            WHERE
                characters(character_id=?character_id);
            """,
            db,
        ).fetch_all()


def test_invalid_rule_parameter() -> None:
    """Ensure exception is thrown if a rule parameter is misspelled or invalid."""

    db = sqlite3.Connection(":memory:")

    initialize_test_data(db)

    engine = QueryEngine()

    engine.execute_script(
        """
        DEFINE
            Character(?id, ?name)
        WHERE
            characters(id=?id, name=?name);
        """
    )

    with pytest.raises(
        ProgrammingError,
        match=r"character_id is not a valid parameter of rule Character.",
    ):
        engine.query(
            """
            FIND
                ?character_id, ?character_name
            WHERE
                Character(character_id=?character_id, name=?character_name);
            """,
            db,
        ).fetch_all()
