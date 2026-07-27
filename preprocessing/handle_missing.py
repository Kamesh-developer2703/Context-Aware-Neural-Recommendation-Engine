import pandas as pd
import os
from pandas.api.types import is_numeric_dtype

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")

customers_path = os.path.join(PROCESSED_PATH, "customers_clean.csv")
articles_path = os.path.join(PROCESSED_PATH, "articles_clean.csv")
transactions_path = os.path.join(PROCESSED_PATH, "transactions_clean.csv")


def fill_missing(df):
    """
    Fill missing values safely.
    """

    for col in df.columns:
        if is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna("Unknown")
    return df


def main():

    print("=" * 60)
    print("Loading cleaned datasets...")
    print("=" * 60)

    customers = pd.read_csv(customers_path)
    articles = pd.read_csv(articles_path)
    transactions = pd.read_csv(transactions_path)

    print("\nMissing Values Before Filling\n")

    print("Customers")
    print(customers.isnull().sum())

    print("\nArticles")
    print(articles.isnull().sum())

    print("\nTransactions")
    print(transactions.isnull().sum())

    customers = fill_missing(customers)
    articles = fill_missing(articles)
    transactions = fill_missing(transactions)

    customers.to_csv(
        os.path.join(PROCESSED_PATH, "customers_no_missing.csv"),
        index=False
    )

    articles.to_csv(
        os.path.join(PROCESSED_PATH, "articles_no_missing.csv"),
        index=False
    )

    transactions.to_csv(
        os.path.join(PROCESSED_PATH, "transactions_no_missing.csv"),
        index=False
    )

    print("\nMissing Values Successfully Handled!")

    print("\nSaved Files")
    print("customers_no_missing.csv")
    print("articles_no_missing.csv")
    print("transactions_no_missing.csv")


if __name__ == "__main__":
    main()