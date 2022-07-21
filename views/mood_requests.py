import json
import sqlite3

from models.mood import Mood


MOODS = [
    {
        "id": 1,
        "label": "Happy"
    },
    {
        "id": 2,
        "label": "Sad"
    },
    {
        "id": 3,
        "label": "Angry"
    },
    {
        "id": 4,
        "label": "Ok"
    }
]


def get_all_moods():
    """This function will retrieve all the moods"""

    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these its a Black Box
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM moods m
        """)

        # Initialize an empty list to hold all entry representations
        moods = []

        # Convert rows of data into python list.
        dataset = db_cursor.fetchall()

        for row in dataset:

            # Create mood instance from the current row
            # Note that the database fields are specified in exact order of the
            # Parameters defined in the mood class above
            mood = Mood(row['id'], row['label'])

            # add the dictionary representation of the mood to the list
            moods.append(mood.__dict__)
        # Use `json` package to properly serialize list as JSON
        return json.dumps(moods)


def get_single_mood(id):
    """This function will retrieve a single mood by its id"""
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM moods m
        WHERE m.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        mood = Mood(data['id'], data['label'])

        return json.dumps(mood.__dict__)


def delete_mood(id):
    """This function deletes an entry"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM moods
        WHERE id = ?
        """, (id, ))
