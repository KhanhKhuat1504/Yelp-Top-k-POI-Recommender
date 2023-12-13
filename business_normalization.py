import pandas as pd

# Step 1: Read the CSV file
df = pd.read_csv("business_new.csv", low_memory=False)

# Step 2: Normalize the `attributes_Ambience` column
# Convert the string representation of dictionary to actual dictionary, handle NaN and empty strings
df["attributes_Ambience"] = df["attributes_Ambience"].apply(
    lambda x: eval(x) if pd.notnull(x) and x != "" else {}
)

# Normalize and create a new DataFrame
# Explicitly setting dtype to boolean for all Series created from the dictionaries
ambience_df = df["attributes_Ambience"].apply(
    lambda x: pd.Series(x, dtype=pd.BooleanDtype())
    if x
    else pd.Series(dtype=pd.BooleanDtype())
)

# Step 3: Concatenate with original DataFrame
df = pd.concat([df.drop("attributes_Ambience", axis=1), ambience_df], axis=1)

# Notes: Repeat the same process for the 'attributes_BestNights', 'attributes_DietaryRestrictions', 'attributes_HairSpecializesIn', 'attributes_Music', `attributes_GoodForMeal` columns


# Step 4: Normalize the `attributes_BusinessParking` column
def update_parking(entry):
    # Check if entry is not NaN and not an empty string
    if pd.notnull(entry) and entry != "":
        # Evaluate the string representation of the dictionary
        parking_dict = eval(entry)
        # If parking_dict is not None, return True if any parking option is True, otherwise False
        if parking_dict is not None:
            return any(parking_dict.values())
    # If the entry is NaN, an empty string, or None, return False
    return False


# Apply the function to the 'attributes_BusinessParking' column
df["attributes_BusinessParking"] = df["attributes_BusinessParking"].apply(
    update_parking
)

# Removing single quotes from all string entries in the DataFrame
df = df.applymap(lambda x: x.replace("'", "") if isinstance(x, str) else x)

# Step 6: Save the modified DataFrame
df.to_csv("business_final.csv", index=False)
