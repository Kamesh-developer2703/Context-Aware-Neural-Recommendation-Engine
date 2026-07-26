import os
import pandas as pd

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENCODED_PATH = os.path.join(BASE_DIR, "data", "encoded")
FEATURE_PATH = os.path.join(BASE_DIR, "data", "features")

os.makedirs(FEATURE_PATH, exist_ok=True)

articles_file = os.path.join(ENCODED_PATH, "articles_encoded.csv")
transactions_file = os.path.join(ENCODED_PATH, "transactions_encoded.csv")


def main():

    print("=" * 60)
    print("Generating Item Features")
    print("=" * 60)

    articles = pd.read_csv(articles_file)
    transactions = pd.read_csv(transactions_file)

    purchase_frequency = (
        transactions.groupby("article_id")
        .size()
        .reset_index(name="purchase_frequency")
    )

    average_price = (
        transactions.groupby("article_id")["price"]
        .mean()
        .reset_index(name="average_price")
    )

    item_features = articles.merge(
        purchase_frequency,
        on="article_id",
        how="left"
    )

    item_features = item_features.merge(
        average_price,
        on="article_id",
        how="left"
    )

    item_features["purchase_frequency"] = (
        item_features["purchase_frequency"].fillna(0)
    )

    item_features["average_price"] = (
        item_features["average_price"].fillna(0)
    )

    output_file = os.path.join(FEATURE_PATH, "item_features.csv")

    item_features.to_csv(output_file, index=False)

    print("\nItem Features Generated Successfully!")
    print(f"Saved: {output_file}")
    print(f"Shape: {item_features.shape}")


if __name__ == "__main__":
    main()