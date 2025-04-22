import sqlite3

#connects to SQLite database
def connect_db():
    return sqlite3.connect("meals.db")

#combine meal + related data and write to file
def process_data():
    conn = connect_db()
    cur = conn.cursor()


    cur.execute("""
        SELECT Meals.name, Meals.rating, Recipes.dish_type, Recipes.cuisine, 
               Nutrition.calories, Nutrition.fat_g, Nutrition.sugar_g, Nutrition.protein_g
        FROM Meals
        JOIN Recipes ON Meals.id = Recipes.meal_id
        JOIN Nutrition ON Meals.id = Nutrition.meal_id
    """)
    results = cur.fetchall()
    conn.close()

    with open("output.txt", "w") as f:
        for r in results:
            f.write(f"{r[0]} | Rating: {r[1]} | Dish Type: {r[2]} | Cuisine: {r[3]} | Calories: {r[4]} | Fat: {r[5]}g | Sugar: {r[6]}g | Protein: {r[7]}g\n")

if __name__ == "__main__":
    process_data()