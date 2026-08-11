import os
import pandas as pd


# -----------------------------
# Transactions
# -----------------------------

TRANSACTIONS_FILE = "data/encoded/transactions_encoded.csv"

_transactions_cache = None


def _load_transactions():
    global _transactions_cache

    if _transactions_cache is None:
        if not os.path.exists(TRANSACTIONS_FILE):
            return pd.DataFrame()

        _transactions_cache = pd.read_csv(TRANSACTIONS_FILE)

    return _transactions_cache


# -----------------------------
# Recommendations
# -----------------------------

FILE = "outputs/recommendations.csv"

_recommendations_cache = None


def _load_recommendations():
    global _recommendations_cache

    if _recommendations_cache is None:
        if not os.path.exists(FILE):
            return pd.DataFrame()

        _recommendations_cache = pd.read_csv(FILE)

    return _recommendations_cache


def get_recommendations(customer_id=None):
    df = _load_recommendations()

    if df.empty:
        return []

    if customer_id is not None and "customer_id" in df.columns:
        df = df[df["customer_id"] == customer_id]

    if "score" in df.columns:
        df = df.sort_values(
            "score",
            ascending=False
        )

    return df.to_dict(orient="records")


# -----------------------------
# Trending
# -----------------------------

def get_trending(limit=10):
    df = _load_transactions()

    if df.empty:
        return []

    if "article_id" not in df.columns:
        return []

    trending = (
        df.groupby("article_id")
        .size()
        .reset_index(name="interaction_count")
        .sort_values(
            "interaction_count",
            ascending=False
        )
    )

    return trending.head(limit).to_dict(
        orient="records"
    )