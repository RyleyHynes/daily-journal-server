import json
import sqlite3

from models.tag import Tag


def get_all_tags():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. Its a Black Box
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            t.id,
            t.name
        FROM tags t
                """)
        # Initialize an empty list to hold all tag representations
        tags = []

        # Convert rows of data into a python list
        dataset = db_cursor.fetchall()

        # Iterate the list of data returned form the database
        for row in dataset:
            # Create an entry instance from the current row
            tag = Tag(row['id'], row['name'])

            # add the dictionary representation of the tag to the list
            tags.append(tag.__dict__)

    return json.dumps(tags)


def get_single_tag(id):
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. Its a Black Box
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            t.id,
            t.name
        FROM tags t
        WHERE t.id = ?
        """, (id, ))

        # Convert rows of data into a python list
        row = db_cursor.fetchone()

        # Create an entry instance from the current row
        tag = Tag(row['id'], row['name'])

        return json.dumps(tag.__dict__)
