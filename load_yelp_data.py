import sqlite3

#connects to SQLite database
def connect_db():
    return sqlite3.connect("mealsreal.db")

#combine meal + related data and write to file
def process_data():
    conn = connect_db()
    cur = conn.cursor()

    # Insert sample data into Meals table
    meals_to_insert = [
        ("Mac & Cheese", "Zingerman's", 4.5),
        ("Spicy Ramen", "Slurping Turtle", 4.7),
        ("Bulgogi Bowl", "Tomukun", 4.6),
        ("Avocado Toast", "Fred's Diner", 4.2),
        ("Tikka Masala", "Cardamom", 4.8)
    ]

    for name, restaurant, rating in meals_to_insert:
        cur.execute("""
            INSERT OR IGNORE INTO Meals (name, restaurant, rating)
            VALUES (?, ?, ?)
        """, (name, restaurant, rating))

    conn.commit()  

    # Now fetch and write results from joined tables
    cur.execute("""
        SELECT Meals.name, Meals.rating, Recipes.popularity, Nutrition.calories, 
               Nutrition.fat_g, Nutrition.sugar_g, Nutrition.protein_g
        FROM Meals
        JOIN Recipes ON Meals.id = Recipes.meal_id
        JOIN Nutrition ON Meals.id = Nutrition.meal_id
    """)
    results = cur.fetchall()
    conn.close()

    with open("output.txt", "w") as f:
        for r in results:
            f.write(f"{r[0]} | Rating: {r[1]} | Popularity: {r[2]} | Calories: {r[3]} | Fat: {r[4]}g | Sugar: {r[5]}g | Protein: {r[6]}g\n")

if __name__ == "__main__":
    process_data()