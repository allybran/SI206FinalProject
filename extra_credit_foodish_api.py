import sqlite3
import requests
import time

def connect_db():
    return sqlite3.connect("meals.db")

def get_foodish_images():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS FoodImages")
    cur.execute("""
        CREATE TABLE FoodImages (
            meal_id INTEGER PRIMARY KEY,
            image_url TEXT
        )
    """)

    cur.execute("SELECT id FROM Meals")
    meals = cur.fetchall()

    new_inserts = 0
    for meal in meals:
        if cur.rowcount == 1:
            new_inserts +=1
        if new_inserts >= 25:  # just grab 25 random images
            break

        meal_id = meal[0]
        response = requests.get("https://foodish-api.com/api/")
        if response.status_code == 200: #200 means it passes
            image_url = response.json().get("image", "")
            cur.execute("INSERT OR IGNORE INTO FoodImages (meal_id, image_url) VALUES (?, ?)", (meal_id, image_url))
            print(f"Added image for meal ID: {meal_id}")
            count += 1
        time.sleep(0.5)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    get_foodish_images()
