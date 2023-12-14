import pandas as pd

from sqlite3 import dbapi2 as sq3

connection = sq3.connect('yelp_database.db')

cursor = connection.cursor()

query = "SELECT * FROM businesses ORDER BY stars DESC LIMIT 20"

df = pd.read_sql_query(query, connection)


print(df[['business_id', 'city', 'name', 'stars']])


#print(df.head()['categories'])
#print(df.head()['DietaryRestrictions'])

#cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='businesses'")
#print(cursor.fetchone()[0])

connection.close()