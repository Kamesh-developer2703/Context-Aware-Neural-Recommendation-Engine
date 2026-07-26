import os
import pandas as pd

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENCODED_PATH = os.path.join(BASE_DIR, "data", "encoded")
FEATURE_PATH = os.path.join(BASE_DIR, "data", "features")

os.makedirs(FEATURE_PATH, exist_ok=True)

transactions_file = os.path.join(
    ENCODED_PATH,
    "transactions_encoded.csv"
)


def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"


def main():

    print("=" * 60)
    print("Generating Contextual Features")
    print("=" * 60)

    transactions = pd.read_csv(transactions_file)

    # Convert to datetime
    transactions["t_dat"] = pd.to_datetime(
        transactions["t_dat"]
    )

    # Date-based features
    transactions["year"] = transactions["t_dat"].dt.year
    transactions["month"] = transactions["t_dat"].dt.month
    transactions["day"] = transactions["t_dat"].dt.day
    transactions["day_of_week"] = (
        transactions["t_dat"].dt.dayofweek
    )

    transactions["is_weekend"] = (
        transactions["day_of_week"] >= 5
    ).astype(int)

    transactions["season"] = (
        transactions["month"]
        .apply(get_season)
    )

    output_file = os.path.join(
        FEATURE_PATH,
        "contextual_features.csv"
    )

    transactions.to_csv(output_file, index=False)

    print("\nContextual Features Generated Successfully!")
    print(f"Saved: {output_file}")
    print(f"Shape: {transactions.shape}")


if __name__ == "__main__":
    main()