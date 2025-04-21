# this will be where we visualize the data 

import sqlite3
import pandas as pd 
import seaborn as sns
import matplotlib.pylot as plt 

def connect_db():
    return sqlite3.connect("meals.db") #connect to meals database

def load_data_for_visualization(): #grab the data we are going to use
    conn = connect_db()
    df = pd.read_sql_query("""
        SELECT Meals.name, Meals.rating, Recipes.popularity, Nutrition.calories, Nutrition.fat_g, Nutrition.sugar_g, Nutrition.protein_g
        FROM Meals
        JOIN Recipes ON Meals.id = Recipes.meal_id
        JOIN Nutrition ON Meals.id = Nutrition.meal_id
    """, conn)
    conn.close()
    return df

def make_visuals(): #creating graphs
    df = load_data_for_visualization()
    #bar chart of 10 most popular recipes 
    top10 = df.sort_values("popularity", ascending=False).head(10)
    sns.barplot(data=top10, x="name", y="popularity")
    plt.xticks(rotation=45, ha='right')  # rotate labels for readability
    plt.title("Top 10 Recipes by Popularity")
    plt.tight_layout()
    plt.show()

     # Scatterplot - calories vs popularity
    sns.scatterplot(data=df, x="calories", y="popularity")
    plt.title("Calories vs Popularity")
    plt.tight_layout()
    plt.show()







