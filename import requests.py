#SI 206 Final Project
#Lauren Starr and Ally Brangham
#Group Name: Ann Arbor Foodies



import sqlite3
import json 
import requests

# I made an account to download a free API key from Nutritionix
#Below are my personal credentials 

app_id = "7b857982"
app_key = "147987eb843d733fd4bd746545c15e0d"

#connects to the database
def connect_db():
    conn = sqlite3.connect("meals.db")
    cur = conn.cursor()
    return conn, cur

#searching nutrition info for each popular meal 
def search_food(food_item): 
    conn, cur = connect_db()
    cur.execute("SELECT id, name FROM meals")
    meals = cur.fetchall()
    
    headers = {
        "x-app-id": app_id,
        "x-app-key": app_key,
        "Content-Type": "application/json",
    }
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients" 

    data = {
        "query": food_item
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200: #status code 200 means the request worked
        result = response.json()


        if result["foods"]: 
            food = result["foods"][0] #this is going to accept the first match of the search
            #print nutrition info
            print(f"Nutrition info for: {food['food_name'].title()}")
            print(f"Calories: {food['nf_calories']} kcal")
            print(f"Total fat: {food['nf_total_fat']} grams")
            print(f"Sugar: {food['nf_sugars']} grams")
            print(f"Protein: {food['nf_protein']} grams")
        else: 
            print("No results found")
    else:
        print("Error:", response.status_code, response.text)
    
#sample practice: 
search_food("French fries")

        