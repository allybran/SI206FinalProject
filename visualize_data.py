# this will be where we visualize the data 

import sqlite3
import pandas as pd 
import seaborn as sns
import matplotlib.pylot as plt 

def connect_db():
    return sqlite3.connect("meals.db") #connect to meals database

def load_data_for_visualization()
    conn = connect_db()
    df = pd.read_sql_query("""
        SELECT Meals.name, Meals.rating, Recipes.popularity, Nutrition.calories, Nutrition.fat_g, Nutrition.sugar_g, Nutrition.protein_g
        FROM Meals
        JOIN Recipes ON Meals.id = Recipes.meal_id
        JOIN Nutrition ON Meals.id = Nutrition.meal_id
    """, conn)
    conn.close()
    return df

