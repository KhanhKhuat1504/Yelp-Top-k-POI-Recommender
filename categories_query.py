import pandas as pd
from sqlite3 import dbapi2 as sqlite
from pathlib import Path

connnection = sqlite.connect("yelp.db")
import pandas as pd

from sqlite3 import dbapi2 as sq3

connection = sq3.connect("yelp_database.db")

cursor = connection.cursor()

# # Get user input and split it into categories
# user_input = input("Enter the categories for your location of interest: ")
# categories = user_input.split()  # Splits on any whitespace, including spaces and tabs

categories = [
    "Restaurants",
    "Tacos",
    "Tex-Mex",
]

# Calculate the weighted score
# weighted_score_query = "0.7 * review_count + 0.3 * stars"

# Create a subquery to count the matches for each business
match_count_query = " + ".join(
    [
        f"(CASE WHEN categories LIKE '%{category}%' THEN 1 ELSE 0 END)"
        for category in categories
    ]
)

# Create the main query
query = f"""
SELECT *, ({match_count_query}) AS match_count
FROM businesses
WHERE ({match_count_query}) > 0
ORDER BY match_count DESC LIMIT 10
"""

df = pd.read_sql_query(query, connection)


print(df[["business_id", "name", "stars"]])


# print(df.head()['categories'])
# print(df.head()['DietaryRestrictions'])

# cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='businesses'")
# print(cursor.fetchone()[0])

connection.close()
