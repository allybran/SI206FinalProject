import requests
import sqlite3

# Make API request for full page HTML content
url = "https://en.wikipedia.org/w/api.php"
params = {
    "action": "parse",
    "page": "Tourism_in_the_United_States",
    "format": "json",
    "prop": "wikitext"  # pull the raw wikitext
}

response = requests.get(url, params=params)
data = response.json()
wikitext = data["parse"]["wikitext"]["*"]



# Manually collected data 
city_data = {
    "New York City": 65.2,
    "Miami": 24.2,
    "Los Angeles": 50.1,
    "Orlando": 75.0,
    "Las Vegas": 42.5,
    "Chicago": 57.6
}

conn = sqlite3.connect('tourism_data.db')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS Tourism (
        city TEXT PRIMARY KEY,
        tourists_millions REAL
    )
''')

for city, visitors in city_data.items():
    cur.execute("INSERT OR IGNORE INTO Tourism (city, tourists_millions) VALUES (?, ?)", (city, visitors))

conn.commit()
conn.close()
#printing daya from the Wikipedia site
print("\n Stored the following U.S. city tourism numbers in the database:")
for city, visitors in city_data.items():
    print(f"{city}: {visitors} million visitors")