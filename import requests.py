import requests
import json 
import time 

# I made an account to download a free API key from Nutritionix
#Below are my personal credentials 

app_id = "7b857982"
app_key = "147987eb843d733fd4bd746545c15e0d"

#searching nutrition info for each popular meal 
def search_food(food_item): 
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

    headers = {
        "x-app-id": app_id,
        "x-app-key": app_key,
        "Content-Type": "application/json",
    }

    data = {
        "query": food_item
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200: #status code 200 means the request worked
        result = response.json()
        if result["foods"]: 
            food = result["food"] #this is jgoing to accept the first match of the search
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

        