#SI 206 Final Project
#Lauren Starr and Ally Brangham
#Group Name: Ann Arbor Foodies




import sqlite3
import json
import requests
import pandas as pd
import seaborn as sns
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
    

#searching nutrition info for each popular meal 
def get_nutrition_facts(): 
    conn, cur = connect_db()
    cur.execute("SELECT id, name FROM meals") #gets IF name and meals from the 
    meals = cur.fetchall()

    headers = {
        "x-app-id": app_id,
        "x-app-key": app_key,
        "Content-Type": "application/json",
    }
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients" 
    count = 0
    
    for meal_id, food_item in meals: 
        try: 
            response =requests.post(url, headers=headers, json={"query":food_item})
            food = response.json()["foods"][0] #this is going to accept the first match of the search
            cur.execute("""
                INSERT OR IGNORE INTO Nutrition (meal_id, calories, fat_grams, sugar_grams, protein_grams 
                FROM meals 
                JOIN Nutrition ON Meals.id = Nutrition.meal_id
            """, conn)
            conn.close()
            return df 