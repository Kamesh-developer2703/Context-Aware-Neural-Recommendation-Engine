import os
import pandas as pd

from ann.recommender import get_dynamic_recommendations
from api.cache import load_recommendations


FILE = "outputs/recommendations.csv"


def get_recommendations(customer_id=None, limit=10):

    # -----------------------------------------
    # Dynamic customer recommendation
    # -----------------------------------------

    if customer_id is not None:

        recommendations = get_dynamic_recommendations(
            customer_id,
            limit
        )

        if recommendations is None:
            return []

        return recommendations

    # -----------------------------------------
    # Global recommendations
    # -----------------------------------------

    if not os.path.exists(FILE):
        raise FileNotFoundError(
            "Recommendation file not found."
        )

    df = load_recommendations()

    if df.empty:
        return []

    df = df.sort_values(
        "score",
        ascending=False
    )

    return df.head(limit).to_dict(
        orient="records"
    )