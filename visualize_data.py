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
        SELECT Meals.name, Meals.rating, Nutrition.calories, Nutrition.fat_g, Nutrition.sugar_g, Nutrition.protein_g
        FROM Meals
        JOIN Nutrition ON Meals.id = Nutrition.meal_id
    """, conn)
    conn.close()
    return df

def make_visuals(): #creating graphs

    df = load_data_for_visualization()

    print(df.head()) #debug check
    print(df.shape)

    #trying to convert columns to numbers 
    numeric_columns = ["fat_g", "sugar_g", "protein_g"]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    #bar chart of 10 most popular recipes 
    plt.figure(figsize=(12,6)) 
    sns.barplot(data=top10, x="name", y="rating")
    plt.xticks(rotation=45, ha='right')
    plt.title("Top 10 Meals by Yelp Rating")
    plt.tight_layout()
    plt.show()

    # Scatterplot - calories vs popularity
    sns.scatterplot(data=df, x="calories", y="rating")
    plt.title("Calories vs Yelp Rating")
    plt.tight_layout()
    plt.show()

    # stacked bar chart - 10 meals with macronutrients 
    df.set_index("name")[["fat_g", "sugar_g", "protein_g"]].head(10).plot(kind="bar", stacked=True)
    plt.title("Macronutrient Breakdown (Top 10 Meals)")
    plt.ylabel("Grams")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    make_visuals()







