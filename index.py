import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import json
from sqlite3 import dbapi2 as sq3
from pathlib import Path
from collections import OrderedDict

import tensorflow as tf
from tensorflow import keras

from time import time
from IPython.display import clear_output

#Dataset Doc: https://www.yelp.com/dataset/documentation/main
REVIEW_PATH = 'yelp_academic_dataset_review.json'        
BUSINESS_PATH = 'yelp_academic_dataset_business.json'            
USER_PATH = 'yelp_academic_dataset_user.json'

def load_rows(file_path, nrows=None, only_return_count=False, verbose=True):
    """
    Returns dataframe from json file
    """
    tic = time()
    with open(file_path, 'r', encoding='utf-8') as json_file:
        count = 0
        objs = []
        line = json_file.readline()
        while (nrows is None or count<nrows) and line:
            count += 1
            if not only_return_count:
                obj = json.loads(line)
                objs.append(obj)
            line = json_file.readline()
        toc = time()
        if verbose:
            print(file_path.split('/')[-1], 'loaded. Count =', count, ', Time =', round(toc-tic,2), 'secs.')
        
        if only_return_count:
            return count
        
        return pd.DataFrame(objs)
    
#data generator to load data in chunks
def load_rows_gen(file_path, nrows=1e6, verbose=True):
    """
    Returns data in chunks
    """
    with open(file_path) as json_file:
        line = json_file.readline()
        total = 0
        while line:
            count = 0
            objs = []
            tic = time()
            while count<nrows and line:
                count+=1
                obj = json.loads(line)
                objs.append(obj)
                line = json_file.readline()
                total += count
            toc = time()
            print('Loaded chunk of size:', count, ", Time =", round(toc-tic,2), 'secs.')
            yield pd.DataFrame(objs)

PATHSTART = "."
def get_db(dbfile):
    #get connection to db
    sqlite_db = sq3.connect(Path(PATHSTART)/ dbfile)
    return sqlite_db

def init_db(dbfile, schema):
    #create db a/c to schema
    db = get_db(dbfile)
    
    #execute sql code
    c = db.cursor()
    c.executescript(schema)
    
    #make commit
    db.commit()
    return db

def make_query(db, sel):
    c = db.cursor().execute(sel)
    return c.fetchall()

from collections import OrderedDict
def make_frame(list_of_tuples, legend):
    framelist=[]
    for i, cname in enumerate(legend):
        framelist.append((cname,[e[i] for e in list_of_tuples]))
    return pd.DataFrame.from_dict(OrderedDict(framelist)) 

users_schema = """
DROP TABLE IF EXISTS "users";

CREATE TABLE "users" (
    "user_id" INTEGER PRIMARY KEY NOT NULL,
    "name" VARCHAR,
    "review_count" INTEGER,
    "yelping_since" TIMESTAMP,
    "useful" INTEGER,
    "funny" INTEGER,
    "cool" INTEGER,
    "elite" VARCHAR,
    "friends" VARCHAR,
    "fans" INTEGER,
    "average_stars" FLOAT,
    "compliment_hot" INTEGER,
    "compliment_more" INTEGER, 
    "compliment_profile" INTEGER,
    "compliment_cute" INTEGER,
    "compliment_list" INTEGER,
    "compliment_note" INTEGER,
    "compliment_plain" INTEGER,
    "compliment_cool" INTEGER,
    "compliment_funny" INTEGER,
    "compliment_writer" INTEGER,
    "compliment_photos" INTEGER
);
"""
businesses_schema="""
DROP TABLE IF EXISTS "businesses";

CREATE TABLE "businesses" (
    "business_id" INTEGER PRIMARY KEY NOT NULL,
    "name" VARCHAR,
    "address" VARCHAR,
    "city" VARCHAR,
    "state" VARCHAR,
    "postal_code" VARCHAR,
    "latitude" FLOAT,
    "longitude" FLOAT,
    "stars" FLOAT,
    "review_count" INTEGER,
    "is_open" BOOLEAN,
    "categories" VARCHAR,
"""

reviews_schema = """
DROP TABLE IF EXISTS "reviews";

CREATE TABLE "reviews" (
    "review_id" VARCHAR PRIMARY KEY,
    "user_id" INTEGER,
    "business_id" INTEGER,
    "stars" FLOAT,
    "useful" INTEGER,
     "funny" INTEGER,
    "cool" INTEGER,
    "text"  VARCHAR,
    "date" TIMESTAMP,
    
    
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (business_id) REFERENCES businesses(business_id)
);
"""
schema_close = ");"

# #Load data about all businesses
# business_df = load_rows(BUSINESS_PATH)
# business_df.head()

# #Here we preprocess our businesses data
# def preprocess_business_df(df):
#     """
#     Preprocess data from BUSINESS_PATH
#     returns final DataFrame
#     """
#     #Changing business_id to numbers
#     global businessid_to_idx
#     businessid_to_idx = {b_id : idx for idx, b_id in enumerate(df.business_id.unique())}
#     df.business_id = df.business_id.map(lambda x: businessid_to_idx[x])

#     #TDT
#     df.is_open = df.is_open.astype(bool)

#     # Exploding attributes [MultiCategorization]
#     attr = [col for col in df.attributes.explode().unique() if col is not None]
#     lst_of_attr_dict = []
#     for attr_dict in df.attributes:
#         if not attr_dict:
#             lst_of_attr_dict.append({})
#         continue

#     if 'BusinessParking' in attr_dict:
#         if type(attr_dict['BusinessParking']) == str:
#             attr_dict['BusinessParking'] = ('True' in attr_dict['BusinessParking'])

#     lst_of_attr_dict.append(attr_dict)

#     attr_df = pd.DataFrame(lst_of_attr_dict, columns=attr)
#     for col in attr_df:
#         #Handling missing
#         #Strategy -> absence of attribute means restauratn doesn't have it
#         #ex. If parking is null then restaurant doesn't have parking
#         attr_df[col] = attr_df[col].fillna(False).astype(bool)
    
#     df = pd.concat([df.reset_index().drop('index', axis=1), attr_df], axis=1)
#     df.drop(['attributes'], axis=1, inplace=True)
    
#     #Exploding hours ie. getting opening and closing time for various days
#     lst_of_time = []
#     for time_dict in df.hours:
#         if not time_dict:
#             lst_of_time.append({})
#             continue
#         lst_of_time.append(time_dict)
#     time_df = pd.DataFrame(lst_of_time)
#     df = pd.concat([df, time_df], axis=1).drop('hours', axis=1)
#     return df

# business_df = preprocess_business_df(business_df)
# print(business_df.info())

# # Completing Business Table Schema
# for bool_col in business_df.columns[12:51]:
#     businesses_schema += '    \"' + bool_col + '\"' + ' BOOLEAN,\n'
# for day in business_df.columns[51:]:
#     businesses_schema += '    \"' + day + '\"' + ' VARCHAR,\n'
    
# businesses_schema = businesses_schema[:-2] + schema_close

# #Create db
# db = init_db("yelp_database.db", users_schema+businesses_schema+reviews_schema)

#business data to sql
# business_df.to_sql('businesses', db, if_exists='append', index=False)

#release memory
# del business_df


user_df = load_rows(USER_PATH)
def preprocess_user_df(df):
    """
    Preprocess data from BUSINESS_PATH
    returns final DataFrame
    """
    #Changing business_id to numbers
    global userid_to_idx
    userid_to_idx = {b_id : idx for idx, b_id in enumerate(df.user_id.unique())}
    df.user_id = df.user_id.map(lambda x: userid_to_idx[x])
    return df

user_df = preprocess_user_df(user_df)
connection = sq3.connect('yelp_database.db')
user_df.to_sql('users', connection, if_exists='append', index=False)

query = "SELECT * FROM users"
user_df = pd.read_sql_query(query, connection)

print(user_df.head())

connection.close()


