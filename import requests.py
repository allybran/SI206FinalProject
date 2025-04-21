#SI 206 Final Project
#Lauren Starr and Ally Brangham
#Group Name: Ann Arbor Foodies



import sqlite3
import json
import requests
#import pandas as pd
#import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

# We made an account to download a free API key from Nutritionix
#Below are our personal credentials 

app_id = "7b857982"
app_key = "147987eb843d733fd4bd746545c15e0d"

#connects to the database
def connect_db():
    conn = sqlite3.connect("meals.db")
    cur = conn.cursor()
    return conn, cur

# create meals and nutrition tables
def create_tables():
    conn, cur = connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            restaurant TEXT,
            rating REAL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Nutrition (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER,
            calories INTEGER,
            fat_g REAL,
            sugar_g REAL,
            protein_g REAL,
            FOREIGN KEY(meal_id) REFERENCES Meals(id)
        )
    """)
    conn.commit()
    conn.close()

    # load meals from custom JSON file  
    #limits to 25 per run
def load_meals_json(filename="yelp_data.json"):
    with open(filename, "r") as f:
        all_meals = json.load(f)

    conn, cur = connect_db()
    count = 0
    for item in all_meals:
        if item.get("restaurant name") and item.get("Popular_dish") and isinstance(item.get("rating"), (int, float)):
            try:
                #insert data into a "Meals" table
                cur.execute("INSERT OR IGNORE INTO Meals (name, restaurant, rating) VALUES (?, ?, ?)", 
                            (item["Popular_dish"], item["restaurant name"], item["rating"]))
                count += 1
                if count >= 25: #project requirement
                    break 
            except:
                continue
    conn.commit()
    conn.close()
    

#opening the api and storing data 
def get_nutrition_facts(): 
    conn, cur = connect_db()
    cur.execute("SELECT id, name FROM meals") #SQL SELECT query
    meals = cur.fetchall()
    
    #inputting my personalized api keys
    headers = {
        "x-app-id": app_id,
        "x-app-key": app_key,
        "Content-Type": "application/json",
    }
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients" 
    count = 0 #keeping track of how many foods i put into the api 
    
    for meal_id, food_item in meals: #loop through each meal in the database
        try: 
            response =requests.post(url, headers=headers, json={"query":food_item})
            food = response.json()["foods"][0] #this is going to accept the first match of the search
            #inserting nutrition info with SQL parameters
            cur.execute(""" 
                INSERT OR IGNORE INTO Nutrition (meal_id, calories, fat_grams, sugar_grams, protein_grams)
                VALUES (?, ?, ?, ?, ?)
            """,(meal_id, food["nf_calories"], food["nf_total_fat"], food["nf_sugars"], food["nf_protein"]))
            count += 1 
            if count >= 25: 
                break
        except: 
            continue
conn.commit()
conn.close()

#combine meal + nutrition data and write it to a text file
#edit
def process_data():
    conn = sqlite3.connect("meals.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT Meals.name, Meals.rating, Nutrition.calories, Nutrition.fat_g, Nutrition.sugar_g, Nutrition.protein_g
        FROM Meals
        JOIN Nutrition ON Meals.id = Nutrition.meal_id
    """)
    results = cur.fetchall()
    conn.close()

    with open("output.txt", "w") as f:
        for r in results:
            f.write(f"{r[0]} | Rating: {r[1]} | Calories: {r[2]} | Fat: {r[3]}g | Sugar: {r[4]}g | Protein: {r[5]}g\n")
