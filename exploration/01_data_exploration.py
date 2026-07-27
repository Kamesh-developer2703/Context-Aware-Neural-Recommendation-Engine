import pandas as pd
import os

DATA_PATH = "data/raw"

customers = pd.read_csv(os.path.join(DATA_PATH, "customers.csv"))
articles = pd.read_csv(os.path.join(DATA_PATH, "articles.csv"))

# Load only first 100000 rows for exploration
transactions = pd.read_csv(
    os.path.join(DATA_PATH, "transactions_train.csv"),
    nrows=100000
)

print("="*60)
print("DATASET SHAPES")
print("="*60)

print("Customers :", customers.shape)
print("Articles :", articles.shape)
print("Transactions :", transactions.shape)

print("\nCUSTOMERS")
print(customers.head())

print("\nARTICLES")
print(articles.head())

print("\nTRANSACTIONS")
print(transactions.head())

print("\nMissing Values")

print(customers.isnull().sum())

print(articles.isnull().sum())

print(transactions.isnull().sum())

print("\nDuplicate Values")

print("Customers :", customers.duplicated().sum())
print("Articles :", articles.duplicated().sum())
print("Transactions :", transactions.duplicated().sum())

print("\nUnique Customers :", customers["customer_id"].nunique())

print("Unique Articles :", articles["article_id"].nunique())

print("Transactions Loaded :", len(transactions))

print("\nCustomer IDs Valid :",
      transactions["customer_id"].isin(customers["customer_id"]).all())

print("Article IDs Valid :",
      transactions["article_id"].isin(articles["article_id"]).all())