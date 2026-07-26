import os
import pandas as pd

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENCODED_PATH = os.path.join(BASE_DIR, "data", "encoded")
FEATURE_PATH = os.path.join(BASE_DIR, "data", "features")

os.makedirs(FEATURE_PATH, exist_ok=True)

customers_file = os.path.join(ENCODED_PATH, "customers_encoded.csv")
transactions_file = os.path.join(ENCODED_PATH, "transactions_encoded.csv")


def main():

    print("=" * 60)
    print("Generating User Features")
    print("=" * 60)

    customers = pd.read_csv(customers_file)
    transactions = pd.read_csv(transactions_file)

    # Number of purchases per customer
    purchase_count = (
        transactions.groupby("customer_id")
        .size()
        .reset_index(name="purchase_count")
    )

    # Average spending
    avg_spending = (
        transactions.groupby("customer_id")["price"]
        .mean()
        .reset_index(name="avg_spending")
    )

    # Merge features
    user_features = customers.merge(
        purchase_count,
        on="customer_id",
        how="left"
    )

    user_features = user_features.merge(
        avg_spending,
        on="customer_id",
        how="left"
    )

    # Fill customers with no purchases
    user_features["purchase_count"] = user_features["purchase_count"].fillna(0)
    user_features["avg_spending"] = user_features["avg_spending"].fillna(0)

    output_file = os.path.join(FEATURE_PATH, "user_features.csv")
    user_features.to_csv(output_file, index=False)

    print("\nUser Features Generated Successfully!")
    print(f"Saved: {output_file}")
    print(f"Shape: {user_features.shape}")


if __name__ == "__main__":
    main()