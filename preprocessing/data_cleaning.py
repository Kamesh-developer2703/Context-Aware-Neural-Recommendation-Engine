import os
import pandas as pd

RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"

os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

print("=" * 60)
print("Loading datasets...")
print("=" * 60)

customers = pd.read_csv(os.path.join(RAW_DATA_PATH, "customers.csv"))
articles = pd.read_csv(os.path.join(RAW_DATA_PATH, "articles.csv"))
transactions = pd.read_csv(os.path.join(RAW_DATA_PATH, "transactions_train.csv"))

print("Datasets loaded successfully!")

print("\nCleaning customers dataset...")

customers["club_member_status"] = customers["club_member_status"].fillna("UNKNOWN")

customers["fashion_news_frequency"] = customers[
    "fashion_news_frequency"
].fillna("NONE")

customers["age"] = customers["age"].fillna(
    customers["age"].median()
)

customers["FN"] = customers["FN"].fillna(0)

customers["Active"] = customers["Active"].fillna(0)

print("Cleaning articles dataset...")

articles["detail_desc"] = articles["detail_desc"].fillna(
    "No Description"
)

print("Cleaning transactions dataset...")

transactions.drop_duplicates(inplace=True)

transactions["t_dat"] = pd.to_datetime(
    transactions["t_dat"]
)

customers.to_csv(
    os.path.join(PROCESSED_DATA_PATH, "customers_processed.csv"),
    index=False
)

articles.to_csv(
    os.path.join(PROCESSED_DATA_PATH, "articles_processed.csv"),
    index=False
)

transactions.to_csv(
    os.path.join(PROCESSED_DATA_PATH, "transactions_processed.csv"),
    index=False
)

print("=" * 60)
print("Data Cleaning Completed Successfully!")
print("=" * 60)