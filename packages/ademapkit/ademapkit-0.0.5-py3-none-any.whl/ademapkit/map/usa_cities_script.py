import json
import sqlite3
import importlib.resources as resources

def usa_cities():
    db_path = resources.files('ademapkit').joinpath('ademapkit.db')
    with sqlite3.connect(db_path) as db:
        db.row_factory = sqlite3.Row
        query = """SELECT * FROM usa_cities"""
        fetch_query = db.execute(query).fetchall()

        cities = []
        for city in fetch_query:
            cities.append(dict(city))

        # cities = sorted(cities)
    return(json.dumps(cities, indent=3))

