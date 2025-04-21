
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
