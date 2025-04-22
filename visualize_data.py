# this will be where we visualize the data 

import sqlite3
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 

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

    print(df.head(20))  # shows us what data exists
    print(df.shape)     # shows how many rows & columns

    #trying to convert columns to numbers 
    numeric_columns = ["fat_g", "sugar_g", "protein_g"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

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

    # stacked bar chart - 10 meals with macronutrients 
    df.set_index("name")[["fat_g", "sugar_g", "protein_g"]].head(10).plot(kind="bar", stacked=True)
    plt.title("Macronutrient Breakdown")
    plt.ylabel("Grams")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    make_visuals()







