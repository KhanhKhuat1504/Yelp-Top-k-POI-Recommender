import os

# replace the path to the spark folder in your system
os.environ[
    "SPARK_HOME"
] = "C:\\Users\\lankh\\Downloads\\spark-3.5.0-bin-hadoop3\\spark-3.5.0-bin-hadoop3"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark Session
spark = SparkSession.builder.appName("test").getOrCreate()

# Read the JSON file
df = spark.read.json("yelp_academic_dataset_business.json")

# Flatten the 'attributes' struct
for field in df.schema["attributes"].dataType.fields:
    df = df.withColumn("attributes_" + field.name, col("attributes." + field.name))

# Flatten the 'hours' struct
for field in df.schema["hours"].dataType.fields:
    df = df.withColumn("hours_" + field.name, col("hours." + field.name))

# Drop the original struct columns
df = df.drop("attributes", "hours")

# Show the schema to verify the changes
df.printSchema()

# Show first few rows to verify
df.show(truncate=False)

# Write to CSV
df.coalesce(1).write.csv("business", header=True, mode="overwrite")

# Notes: You will find a business folder in your current directory.
# Inside that folder, you will find a csv file with the flattened data.
# Repeat the same process for the other two files: yelp_academic_dataset_review.json and yelp_academic_dataset_user.json
