import sqlite3


def createDetailTable():
    with sqlite3.connect('ademapkit.db') as db:
        query = """CREATE TABLE IF NOT EXISTS usa_cities(
            id INTEGER PRIMARY KEY,
            city TEXT NOT NULL
        )"""
        db.execute(query)

# createDetailTable()
def deleteTable():
    with sqlite3.connect('ademapkit.db') as db:
        query = """DELETE FROM usa_cities"""
        db.execute(query)
        db.commit()

# deleteTable()


def detailInsert():
    with sqlite3.connect('ademapkit.db') as db:
        db.row_factory = sqlite3.Row
        query = """SELECT * FROM cities"""
        fetch_cities = db.execute(query).fetchall()

        def insertIntoTable(city_details):
            insert_query = """INSERT INTO usa_cities (city) VALUES (?)"""
            db.execute(insert_query, (city_details,))
            
        cities = []
        for fetch_city in fetch_cities:
            if fetch_city['city'] == "":
                continue
            else:
                city = f"{fetch_city['city'].strip()}, {fetch_city['state'].strip()}, USA"
                cities.append(city)


        sorted_cities = sorted(cities)
        for city in sorted_cities:
            insertIntoTable(city)

        db.commit()

# detailInsert()