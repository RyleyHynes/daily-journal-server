import sqlite3
import json

from models.entry import Entry


ENTRIES = [
    {
        "id": 1,
        "concept": "Javascript",
        "entry": "I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.",
        "moodId": 1,
        "date": "Wed Sep 15 2021 10:10:47 "
    },
    {
        "id": 2,
        "concept": "Python",
        "entry": "Python is named after the Monty Python comedy group from the UK. I'm sad because I thought it was named after the snake",
        "moodId": 4,
        "date": "Wed Sep 15 2021 10:11:33 "
    },
    {
        "id": 3,
        "concept": "Python",
        "entry": "Why did it take so long for python to have a switch statement? It's much cleaner than if/elif blocks",
        "moodId": 3,
        "date": "Wed Sep 15 2021 10:13:11 "
    },
    {
        "id": 4,
        "concept": "Javascript",
        "entry": "Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.",
        "moodId": 3,
        "date": "Wed Sep 15 2021 10:14:05 "
    }
]


def get_all_entries():
    """This function will retrieve all journal entries"""

    # Open a connection to the database
    with sqlite3.connect("http://localhost:8088/entries") as conn:

        # Just use these its a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry
            e.mood_id,
            e.date
        FROM journal_entries e
        """)

        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into python list.
        dataset = db_cursor.fetchall()

        for row in dataset:

            # Create entry instance from the current row.
            # Note that the database fields are specified in exact order of the
            # Parameters defined in the entry class above
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['mood_id'], row['date'])

            # Add the dictionary representation of the entry to the list
            entries.append(entry.__dict__)
        # Use `json` package to properly serialize list as JSON
        return json.dumps(entries)
