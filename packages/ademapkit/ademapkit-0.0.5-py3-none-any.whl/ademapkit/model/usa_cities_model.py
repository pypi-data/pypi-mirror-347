import sqlite3
import json


# Database file path
db_file = "ademapkit.db"
json_file = "usa_states_and_cities.json"

# Connect to SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the table
cursor.execute("""
CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY,
    state TEXT NOT NULL,
    city TEXT NOT NULL
)
""")

# Read the JSON data
with open(json_file, "r") as file:
    data = json.load(file)

# Initialize the ID counter
id_counter = 1

# Iterate through the states and cities
for state, cities in data["countries"]["USA"].items():
    for city in cities:
        cursor.execute("""
        INSERT INTO cities (id, state, city) VALUES (?, ?, ?)
        """, (id_counter, state, city))
        id_counter += 1

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data successfully saved to the database!")
