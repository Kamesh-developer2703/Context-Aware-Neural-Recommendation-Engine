import os
import pandas as pd

# ============================
# Paths
# ============================
PROCESSED = "data/processed"
OUTPUT = "outputs/features"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT, exist_ok=True)

# ============================
# Load Datasets
# ============================
print("=" * 60)
print("Loading processed datasets...")
print("=" * 60)

customers = pd.read_csv(f"{PROCESSED}/customers_processed.csv")
articles = pd.read_csv(f"{PROCESSED}/articles_processed.csv")
transactions = pd.read_csv(f"{PROCESSED}/transactions_processed.csv")

transactions["t_dat"] = pd.to_datetime(transactions["t_dat"])

print("Datasets Loaded Successfully!")

# ============================
# Customer Features
# ============================
print("\nCreating Customer Features...")

customer_features = customers.copy()

customer_features["age_group"] = pd.cut(
    customer_features["age"],
    bins=[0, 18, 25, 35, 50, 100],
    labels=[
        "Teen",
        "Young Adult",
        "Adult",
        "Middle Age",
        "Senior"
    ]
)

# ============================
# Article Features
# ============================
print("Creating Article Features...")

article_features = articles.copy()

article_features["product_name_length"] = (
    article_features["prod_name"]
    .astype(str)
    .str.len()
)

article_features["description_length"] = (
    article_features["detail_desc"]
    .astype(str)
    .str.len()
)

# ============================
# Transaction Features
# ============================
print("Creating Transaction Features...")

transaction_features = (
    transactions
    .groupby("customer_id")
    .agg(
        total_purchases=("article_id", "count"),
        total_spent=("price", "sum"),
        average_price=("price", "mean"),
        unique_products=("article_id", "nunique")
    )
    .reset_index()
)

# ============================
# Merge Customer + Transaction Features
# ============================
print("Merging Features...")

customer_final = customer_features.merge(
    transaction_features,
    on="customer_id",
    how="left"
)

customer_final.fillna(0, inplace=True)

# ============================
# Save Features
# ============================
customer_final.to_csv(
    f"{OUTPUT}/customer_features.csv",
    index=False
)

article_features.to_csv(
    f"{OUTPUT}/article_features.csv",
    index=False
)

transaction_features.to_csv(
    f"{OUTPUT}/transaction_features.csv",
    index=False
)

# ============================
# Summary
# ============================
print("\nFeature Files Created Successfully!")

print("\nCustomer Features Shape:", customer_final.shape)
print("Article Features Shape:", article_features.shape)
print("Transaction Features Shape:", transaction_features.shape)

print("\nSaved Files:")
print(f"- {OUTPUT}/customer_features.csv")
print(f"- {OUTPUT}/article_features.csv")
print(f"- {OUTPUT}/transaction_features.csv")

print("=" * 60)
print("Feature Engineering Completed Successfully!")
print("=" * 60)