import os
import pandas as pd

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

    df = df.sort_values("score", ascending=False)

    return df.to_dict(orient="records")