import sqlite3
import json

def country():
    read_query = """SELECT * FROM country"""
    with sqlite3.connect("ademapkit.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(read_query)
        rows = cursor.fetchall()

        # Convert rows to list of dictionaries
        countries = [dict(row) for row in rows]
    
    return (json.dumps(countries, indent=3))