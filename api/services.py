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
# Personalized Recommendations
# -----------------------------

def get_personalized_recommendations(
    customer_id,
    limit=10,
    favorite_articles=None,
    recently_viewed=None,
    disliked_articles=None
):
    df = _load_recommendations()

    if df.empty:
        return []

    # Customer-specific recommendations
    if "customer_id" in df.columns:
        df = df[df["customer_id"] == customer_id]

    if df.empty:
        return []

    # Recommended item identifier in current dataset
    item_column = "sample_id"

    if item_column not in df.columns:
        return []

    # Remove already-favorited articles
    if favorite_articles:
        df = df[
            ~df[item_column].isin(favorite_articles)
        ]

    # Remove recently viewed articles
    if recently_viewed:
        df = df[
            ~df[item_column].isin(recently_viewed)
        ]

    # Remove disliked articles
    if disliked_articles:
        df = df[
            ~df[item_column].isin(disliked_articles)
        ]

    # Sort by recommendation score
    if "score" in df.columns:
        df = df.sort_values(
            "score",
            ascending=False
        )

    # Remove duplicate recommended items
    df = df.drop_duplicates(
        subset=[item_column]
    )

    return df.head(limit).to_dict(
        orient="records"
    )


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
# -----------------------------
# Similar Articles
# -----------------------------

def get_similar_articles(article_id, limit=10):
    df = _load_transactions()

    if df.empty:
        return None

    if "article_id" not in df.columns:
        return None

    # Check whether requested article exists
    if article_id not in df["article_id"].values:
        return None

    # Customers who interacted with the requested article
    target_customers = set(
        df.loc[
            df["article_id"] == article_id,
            "customer_id"
        ]
    )

    if not target_customers:
        return []

    # Find other articles viewed/bought by the same customers
    similar = df[
        df["customer_id"].isin(target_customers)
        & (df["article_id"] != article_id)
    ]

    if similar.empty:
        return []

    # Count how many common customers interacted with each article
    similar = (
        similar.groupby("article_id")
        .size()
        .reset_index(name="similarity_score")
        .sort_values(
            "similarity_score",
            ascending=False
        )
    )

    return similar.head(limit).to_dict(
        orient="records"
    )