
# get_spoonacular_data.py (fixed version using original structure and keeping new_inserts)

import sqlite3
import requests
import time

# Spoonacular API key
spoonacular_key = "99481001640947f08633a3dffe571ddf"

# Connect to the meals db
def connect_db():
    return sqlite3.connect("meals.db")

def get_spoonacular_data():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM Meals")
    meals = cur.fetchall()

    new_inserts = 0
    for meal in meals:
        if new_inserts >= 25:
            break

        meal_id = meal[0]
        name = meal[1]

        base_url = "https://api.spoonacular.com/recipes/complexSearch"
        params = {
            "query": name,
            "number": 1,
            "addRecipeInformation": True,
            "apiKey": spoonacular_key
        }

        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results")

            if results:
                result = results[0]
                popularity = result.get("aggregateLikes", 0)
                cuisines = result.get("cuisines", [])
                cuisine = cuisines[0] if cuisines else "N/A"

                cur.execute("""
                    INSERT OR IGNORE INTO Recipes (meal_id, popularity, cuisine)
                    VALUES (?, ?, ?)
                """, (meal_id, popularity, cuisine))

                print(f"Added: {name} | Cuisine: {cuisine} | Popularity: {popularity}")
                new_inserts += 1

        else:
            print(f"Error fetching data for {name}: {response.status_code}")

        time.sleep(1.1)

    conn.commit()
    conn.close()
    print("Finished storing Spoonacular data.")

if __name__ == "__main__":
    get_spoonacular_data()
