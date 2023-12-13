import pyodbc
from dotenv import load_dotenv
import os
import util 
import json

load_dotenv()

def connect_to_database():
    # Define your connection details
    server = os.getenv('SERVER')
    database = 'Yelp' 
    username = os.getenv('USERNAME') 
    password = os.getenv('PASSWORD') 

    # Create a connection string
    conn_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # Connect to the SQL Server and return the connection
    return pyodbc.connect(conn_string)

def query_user(cursor, user_id):
    # SQL query to fetch user details
    query = f"SELECT * FROM [user] WHERE user_id = ?"
    cursor.execute(query, (user_id,))

    # Fetch and return the result
    return cursor.fetchone()

def main():
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    # Function to create tables
    def create_tables():
        cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'User')
        CREATE TABLE User (
            user_id NVARCHAR(22) PRIMARY KEY,
            name NVARCHAR(100),
            review_count INT,
            yelping_since DATE,
            useful INT,
            funny INT,
            cool INT,
            fans INT,
            elite NVARCHAR(255), -- Assuming list of years as a string
            average_stars FLOAT,
            compliment_hot INT,
            compliment_more INT,
            compliment_profile INT,
            compliment_cute INT,
            compliment_list INT,
            compliment_note INT,
            compliment_plain INT,
            compliment_cool INT,
            compliment_funny INT,
            compliment_writer INT,
            compliment_photos INT
        )
        ''')
        cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'User_Friends')
        CREATE TABLE User_Friends (
            user_id NVARCHAR(22),
            friend_id NVARCHAR(22),
            PRIMARY KEY (user_id, friend_id),
            FOREIGN KEY (user_id) REFERENCES YelpUser(user_id),
            FOREIGN KEY (friend_id) REFERENCES YelpUser(user_id)
        )
        ''')
        conn.commit()

    # Batch insert functions
    def batch_insert_users(users):
        for user in users:
            cursor.execute('''
                INSERT INTO User (
                    user_id, name, review_count, yelping_since, useful, funny, cool, 
                    fans, elite, average_stars, compliment_hot, compliment_more, 
                    compliment_profile, compliment_cute, compliment_list, 
                    compliment_note, compliment_plain, compliment_cool, 
                    compliment_funny, compliment_writer, compliment_photos
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', 
            
            user['user_id'], user['name'], user['review_count'], user['yelping_since'], 
            user['useful'], user['funny'], user['cool'], user['fans'], 
            ','.join(map(str, user['elite'])), user['average_stars'], 
            user['compliment_hot'], user['compliment_more'], user['compliment_profile'], 
            user['compliment_cute'], user['compliment_list'], user['compliment_note'], 
            user['compliment_plain'], user['compliment_cool'], user['compliment_funny'], 
            user['compliment_writer'], user['compliment_photos']
        )

    def batch_insert_friends(user_id, friends):
        for friend_id in friends:
            cursor.execute('''
                INSERT INTO UserFriends (user_id, friend_id) VALUES (?, ?)
            ''', user_id, friend_id)
        conn.commit()

    # Create tables
    create_tables()

    # Read the JSON file
    with open('path_to_your_json_file.json', 'r') as file:
        data = json.load(file)

    # Insert data in batches
    batch_size = 10000
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        batch_insert_users(batch)
        for user in batch:
            batch_insert_friends(user['user_id'], user['friends'])

    # Close the cursor and connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
