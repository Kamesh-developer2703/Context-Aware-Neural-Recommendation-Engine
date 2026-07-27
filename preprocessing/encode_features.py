import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from pandas.api.types import is_string_dtype, is_object_dtype

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed")
ENCODED_PATH = os.path.join(BASE_DIR, "data", "encoded")

os.makedirs(ENCODED_PATH, exist_ok=True)

customers_file = os.path.join(PROCESSED_PATH, "customers_no_missing.csv")
articles_file = os.path.join(PROCESSED_PATH, "articles_no_missing.csv")
transactions_file = os.path.join(PROCESSED_PATH, "transactions_no_missing.csv")


def encode_dataframe(df, name):

    print(f"\nEncoding {name}...")

    for col in df.columns:

        if is_object_dtype(df[col]) or is_string_dtype(df[col]):

            print(f"Encoding column: {col}")

            le = LabelEncoder()

            df[col] = le.fit_transform(df[col].astype(str))

    return df


def main():

    print("=" * 60)
    print("Encoding Features")
    print("=" * 60)

    customers = pd.read_csv(customers_file)
    articles = pd.read_csv(articles_file)
    transactions = pd.read_csv(transactions_file)

    customers = encode_dataframe(customers, "Customers")
    articles = encode_dataframe(articles, "Articles")
    transactions = encode_dataframe(transactions, "Transactions")

    print("\nEncoded Customers dtypes:")
    print(customers.dtypes)

    print("\nEncoded Articles dtypes:")
    print(articles.dtypes)

    customers.to_csv(
        os.path.join(ENCODED_PATH, "customers_encoded.csv"),
        index=False
    )

    articles.to_csv(
        os.path.join(ENCODED_PATH, "articles_encoded.csv"),
        index=False
    )

    transactions.to_csv(
        os.path.join(ENCODED_PATH, "transactions_encoded.csv"),
        index=False
    )

    print("\nEncoding Completed Successfully!")

    print("\nSaved Files")

    print("customers_encoded.csv")
    print("articles_encoded.csv")
    print("transactions_encoded.csv")


if __name__ == "__main__":
    main()