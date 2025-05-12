import requests
import sqlite3

# CREATE THE COUNTRY TABLE
def createTable():
    createCountryTable = """CREATE TABLE IF NOT EXISTS country(
        id INTEGER PRIMARY KEY,
        continent TEXT NOT NULL,
        country TEXT NOT NULL,
        capital TEXT NOT NULL,
        currency TEXT NOT NULL
    )"""

    with sqlite3.connect("ademapkit.db") as db:
        db.execute(createCountryTable)


def insertCountry():
    url = "https://restcountries.com/v3.1/all"
    createTable()
    try:
        response = requests.get(url)
        response.raise_for_status()
        countries = response.json()

        insert_query = """
            INSERT INTO country(continent, country, capital, currency)
            VALUES (?, ?, ?, ?)
        """

        with sqlite3.connect("ademapkit.db") as db:
            cursor = db.cursor()
            for country in countries:
                name = country.get('name', {}).get('common', 'N/A')
                capital = ", ".join(country.get('capital', ['N/A']))
                
                currencies = country.get('currencies', {})
                currency_list = [f"{info.get('name', 'N/A')} ({code})" for code, info in currencies.items()]
                currency = ", ".join(currency_list) if currency_list else 'N/A'

                continents = country.get('continents', ['N/A'])
                continent = ", ".join(continents)

                data = (continent, name, capital, currency)
                cursor.execute(insert_query, data)

            db.commit()
        return "Success"

    except requests.RequestException as e:
        return f"Error fetching data: {e}"
