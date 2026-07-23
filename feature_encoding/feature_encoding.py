import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# ============================
# Paths
# ============================

FEATURE_PATH = "outputs/features"
OUTPUT_PATH = "outputs/encoded"

os.makedirs(OUTPUT_PATH, exist_ok=True)

print("=" * 60)
print("Loading Feature Files...")
print("=" * 60)

customer = pd.read_csv(f"{FEATURE_PATH}/customer_features.csv")
article = pd.read_csv(f"{FEATURE_PATH}/article_features.csv")
transaction = pd.read_csv(f"{FEATURE_PATH}/transaction_features.csv")

print("Files Loaded Successfully!")

print("\nEncoding Customer Features...")

customer_encoder = LabelEncoder()

customer["club_member_status"] = customer_encoder.fit_transform(
    customer["club_member_status"].astype(str)
)

customer["fashion_news_frequency"] = customer_encoder.fit_transform(
    customer["fashion_news_frequency"].astype(str)
)

customer["age_group"] = customer_encoder.fit_transform(
    customer["age_group"].astype(str)
)

print("Encoding Article Features...")

article_encoder = LabelEncoder()

article["product_type_name"] = article_encoder.fit_transform(
    article["product_type_name"].astype(str)
)

article["product_group_name"] = article_encoder.fit_transform(
    article["product_group_name"].astype(str)
)

article["graphical_appearance_name"] = article_encoder.fit_transform(
    article["graphical_appearance_name"].astype(str)
)

article["colour_group_name"] = article_encoder.fit_transform(
    article["colour_group_name"].astype(str)
)

print("Encoding Transaction Features...")

# Encode sales channel
sales_encoder = LabelEncoder()

transaction["sales_channel_id"] = sales_encoder.fit_transform(
    transaction["sales_channel_id"]
)

# Scale only the price column
scaler = MinMaxScaler()

transaction[["price"]] = scaler.fit_transform(
    transaction[["price"]]
)

# Ensure label is integer
transaction["label"] = transaction["label"].astype(int)

customer.to_csv(
    f"{OUTPUT_PATH}/customer_encoded.csv",
    index=False
)

article.to_csv(
    f"{OUTPUT_PATH}/article_encoded.csv",
    index=False
)

transaction.to_csv(
    f"{OUTPUT_PATH}/transaction_encoded.csv",
    index=False
)

print("\nEncoding Completed Successfully!")

print("Customer Shape :", customer.shape)
print("Article Shape :", article.shape)
print("Transaction Shape :", transaction.shape)

print("\nEncoded Files Saved In:")
print(OUTPUT_PATH)

print("=" * 60)
print("Day 05 Completed Successfully!")
print("=" * 60)