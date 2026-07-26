import os
import pandas as pd

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(PROCESSED_DATA, exist_ok=True)

CUSTOMERS_FILE = os.path.join(RAW_DATA, "customers.csv")
ARTICLES_FILE = os.path.join(RAW_DATA, "articles.csv")
TRANSACTIONS_FILE = os.path.join(RAW_DATA, "transactions_train.csv")


def clean_dataframe(df):
    """Basic cleaning for any dataframe."""

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


def main():

    print("=" * 50)
    print("Loading datasets...")
    print("=" * 50)

    customers = pd.read_csv(CUSTOMERS_FILE)
    articles = pd.read_csv(ARTICLES_FILE)
    transactions = pd.read_csv(TRANSACTIONS_FILE,
    usecols=[
        "t_dat",
        "customer_id",
        "article_id",
        "price",
        "sales_channel_id"
    ],
    dtype={
        "customer_id": "string",
        "article_id": "int32",
        "price": "float32",
        "sales_channel_id": "int8"
    },
    nrows=500000
)

    print("Customers :", customers.shape)
    print("Articles :", articles.shape)
    print("Transactions :", transactions.shape)

    print("\nCleaning datasets...")

    customers = clean_dataframe(customers)
    articles = clean_dataframe(articles)
    transactions = clean_dataframe(transactions)

    customers.to_csv(
        os.path.join(PROCESSED_DATA, "customers_clean.csv"),
        index=False
    )

    articles.to_csv(
        os.path.join(PROCESSED_DATA, "articles_clean.csv"),
        index=False
    )

    transactions.to_csv(
        os.path.join(PROCESSED_DATA, "transactions_clean.csv"),
        index=False
    )

    print("\nCleaning Completed Successfully!")

    print("\nSaved Files")

    print("customers_clean.csv")
    print("articles_clean.csv")
    print("transactions_clean.csv")


if __name__ == "__main__":
    main()