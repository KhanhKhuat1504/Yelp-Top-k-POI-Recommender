import pandas as pd

from sqlite3 import dbapi2 as sq3

connection = sq3.connect('yelp_database.db')

cursor = connection.cursor()

def get_top_results_by_category(city, category):
    # SQL query to fetch records based on the specified category
    query = f"SELECT * FROM businesses WHERE city LIKE '%{city}%' AND categories LIKE '%{category}%' ORDER BY review_count DESC, stars DESC LIMIT 100"

    # Read the query result into a Pandas DataFrame
    df = pd.read_sql_query(query, connection)

    # Display the relevant columns
    if df.empty:
        print(f"No results found for city: {city}")
    else:
        print(df[['business_id', 'name', 'city', 'categories', 'stars', 'review_count']])

# Get user input for the category
user_city = input("Enter a city (e.g., New York): ")

# Get user input for the category
user_category = input("Enter a category (e.g., Restaurants): ")

# Call the function with the user-provided category
get_top_results_by_category(user_city, user_category)

connection.close()