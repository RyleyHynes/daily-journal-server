import sqlite3
import json

from models.entry import Entry
from models.mood import Mood


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
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these its a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label mood_label
        FROM journal_entries e
        JOIN moods m
            ON e.mood_id = m.id
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

            mood = Mood(row['mood_id'], row['mood_label'])

            entry.mood = mood.__dict__

            # Add the dictionary representation of the entry to the list
            entries.append(entry.__dict__)
        # Use `json` package to properly serialize list as JSON
        return json.dumps(entries)


def get_single_entry(id):
    """This function gets a single entry by the entry id"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT 
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date
        FROM journal_entries e
        WHERE e.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        entry = Entry(data['id'], data['concept'],
                      data['entry'], data['mood_id'], data['date'])

        return json.dumps(entry.__dict__)


def delete_entry(id):
    """this function deletes the an entry"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM journal_entries
        WHERE id = ?
        """, (id, ))


def get_entries_with_search(term):
    """This function allows you to search for a term"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date
        FROM journal_entries e
        WHERE e.entry LIKE ?
        """, (f"%{term}%", ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'],
                          row['entry'], row['mood_id'], row['date'])
            entries.append(entry.__dict__)

    return json.dumps(entries)


def create_entry(new_entry):
    """This function creates an entry and accepts a new_entry as a parameter"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO journal_entries
        (concept, entry, mood_id, date)
        VALUES
            (?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], new_entry['date'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added
        # to the database
        id = db_cursor.lastrowid

        new_entry['id'] = id

    return json.dumps(new_entry)


def update_entry(id, new_entry):
    """This function will update the entries"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE journal_entries
            SET
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], new_entry['date'],  ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
