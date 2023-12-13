import pandas as pd
import numpy as np
import seaborn as sns
from pathlib import Path
from collections import OrderedDict
from sklearn.model_selection import train_test_split
import tensorflow as tf 
from keras.layers import Activation
from keras import backend as K
from keras.layers import Input, Embedding, Add, Dot, Flatten, Concatenate, Dense
from keras import Model
from keras.regularizers import l2
from keras.optimizers import Adam, SGD
from keras.utils import plot_model
from sklearn.metrics import mean_squared_error as mse
from time import time
from IPython.display import clear_output
import matplotlib.pyplot as plt
from keras.models import load_model

# Path to the Yelp JSON file
file_path_review = './yelp_academic_dataset_review.csv'
file_path_business = './yelp_academic_dataset_business.csv'
file_path_user = './yelp_academic_dataset_user.csv'

chunk_size = 100000  # Adjust this value based on your system's memory capacity

# Create an empty DataFrame to hold chunks
df_chunks = []

# Function to clean the byte string notation
def clean_byte_notation(s):
    if isinstance(s, str) and s.startswith("b'") and s.endswith("'"):
        return s[2:-1]
    return s

for chunk in pd.read_csv(file_path_review, chunksize=chunk_size, usecols=['user_id', 'business_id', 'stars']
):
    # chunk['user_id'] = chunk['user_id']
    # chunk['business_id'] = chunk['business_id']
    chunk['stars'] =chunk['stars'].astype(int)
    df_chunks.append(chunk)

# Concatenate all chunks into a single DataFrame
df_reviews = pd.concat(df_chunks, ignore_index=True)

nusers = df_reviews['user_id'].nunique()
nrestaurants = df_reviews['business_id'].nunique()

# Create and apply mapping for 'user_id'
df_reviews['user_id'] = pd.factorize(df_reviews['user_id'])[0]
print(f'Max user_id: {df_reviews["user_id"].max()}')

# Create and apply mapping for 'business_id'
df_reviews['business_id'] = pd.factorize(df_reviews['business_id'])[0]
print(f'Max business_id: {df_reviews["business_id"].max()}')

#Train - Val - Test
#80% - 10% - 10%
X_train, X, y_train, y = train_test_split(df_reviews.drop('stars', axis=1), df_reviews.stars, train_size=.8)
X_test, X_val, y_test, y_val = train_test_split(X, y, train_size=.5)
del X, y

print(f"Train Size: {round(X_train.shape[0]/df_reviews.shape[0]*100)}%")
print("X train shape: ", X_train.shape)
print("y train shape: ", y_train.shape)

print(f"\nValidation Size: {round(X_val.shape[0]/df_reviews.shape[0]*100)}%")
print("X val   shape: ", X_val.shape)
print("y val   shape: ", y_val.shape)

# def count_lines_in_file(file_path):
#     line_count = 0
#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             line_count += 1
#     return line_count

# # Count the lines in the file
# total_businesses = count_lines_in_file(file_path_business)

# # Subtract 1 if the file has a header row
# total_businesses -= 1

# print("Total number of businesses:", total_businesses)

# # Helper functions 
# def create_bias(name, inp, n_in, reg):
#     #x = Embedding(n_in, 1, input_length=1, embeddings_regularizer=l2(reg))(inp)
#     x = Embedding(n_in, 1, input_length=1, name=name)(inp)
#     return Flatten(name=name+'_flat')(x)

# def embedding_input(name, n_in, n_out, reg):
#     inp = Input(shape=(1,), dtype='int64', name=name)
#     return inp, Embedding(n_in, n_out, input_length=1, name=name.split('_')[0]+'_factor', embeddings_regularizer=l2(reg))(inp)

# def sigmoid_maker(low, high):
#     def custom_sigmoid(x):
#         return K.sigmoid(x)*(high - low) + low #within range
#     return custom_sigmoid

# # Baseline accuracy using average
mean_rating = y_train.mean()

train_baseline = mse(y_train, [mean_rating]*y_train.shape[0])
val_baseline = mse(y_val, [mean_rating]*y_val.shape[0])
test_baseline = mse(y_test, [mean_rating]*y_test.shape[0])
# print(f"""Baseline MSE using mean rating:\n
#           Train Data: {train_baseline:.4f},
#           Val   Data: {val_baseline:.4f},
#           Test  Data: {test_baseline:.4f}""")

# L = 50 # Embedding dimension
# reg_param = 1e-2 # Regularization constant = 0.01

# # Dense Layer Params
# hidden_layers = 4
# activation = 'relu'
# n_neurons = 32 
# dense_reg = 1e-2

# user_input, uLmat = embedding_input('user_input', nusers, L, reg_param)
# restaurant_input, mLmat = embedding_input('restaurant_input', nrestaurants, L, reg_param)
# user_bias = create_bias('user_bias', user_input, nusers, reg_param)
# restaurant_bias = create_bias('restaurant_bias', restaurant_input, nrestaurants, reg_param)

# x = Concatenate()([Flatten()(uLmat), Flatten()(mLmat)])
# for _ in range(hidden_layers):
#     x = Dense(n_neurons, activation=activation, kernel_regularizer=l2(dense_reg))(x)
# x = Add(name="regression")([user_bias, restaurant_bias, x])
# output = Dense(1, activation=sigmoid_maker(0.5, 5.5), name="Sigmoid_Range")(x)

# model2 = Model([user_input, restaurant_input], output)
# model2.compile(Adam(1e-2), loss='mse')

# model2.summary()

# print(X_train.user_id)

# #training model
# model2.optimizer.learning_rate = 5e-2

# model2.save('Nonlinear_model')

model2_recreated =  load_model("Nonlinear_model")

#Calculating MSE 
ticks = ["Train", "Val", "Test"]
avg_model = [train_baseline, val_baseline, test_baseline]
linear_model, non_linear_model = [], []

for data in [(X_train, y_train), (X_val, y_val), (X_test, y_test)]:
    
    nonlin_mse = mse(data[1], model2_recreated.predict([data[0]['user_id'],data[0]['business_id']], verbose=1))
    non_linear_model.append(nonlin_mse)
    
    clear_output()
    
#Plotting Modelwise Error
plt.figure(figsize=(8,8))
ax = plt.gca()

ax.plot(avg_model, "o-", label="Average Model")
ax.plot(linear_model, "o-", label="Linear Model")
print(linear_model)
ax.plot(non_linear_model, "o-", label="Non-Linear Model")
print(non_linear_model)
ax.set(xlabel='', ylabel='MSE', xticks=[0,1,2], xticklabels=["Train Error", "Val Error", "Test Error"])
ax.legend()
plt.show()