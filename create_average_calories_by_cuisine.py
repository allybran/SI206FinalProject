#creating avg calories by cuisine 

import sqlite3
import pandas as pd 

#connect to the meals db
def connect_db():
    return sqlite3.connect("meals.db")

def create_avg_calories_table():
    conn = connect_db()
    cur = conn.cursor()

    # Remove old table if it exists
    cur.execute("DROP TABLE IF EXISTS AvgCaloriesByCuisine")

    # Query meal calories and cuisine type
    df = pd.read_sql_query("""
        SELECT Recipes.cuisine AS cuisine, Nutrition.calories AS calories
        FROM Meals
        JOIN Nutrition ON Meals.id = Nutrition.meal_id
        JOIN Recipes ON Meals.id = Recipes.meal_id
    """, conn)

    # Calculate avg calories for each cuisine
    avg_df = df.groupby("cuisine")["calories"].mean().reset_index()
    avg_df.columns = ["cuisine", "avg_calories"]

    # Save results into a new table
    avg_df.to_sql("AvgCaloriesByCuisine", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_avg_calories_table()
