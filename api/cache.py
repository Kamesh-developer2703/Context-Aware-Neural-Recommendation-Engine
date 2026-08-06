import pandas as pd

recommendations_cache = None

def load_recommendations():

    global recommendations_cache

    if recommendations_cache is None:

        recommendations_cache = pd.read_csv(
            "outputs/recommendations.csv"
        )

        recommendations_cache["customer_id"] = (
            recommendations_cache["customer_id"].astype(str)
        )

    return recommendations_cache


def refresh_cache():

    global recommendations_cache

    recommendations_cache = pd.read_csv(
        "outputs/recommendations.csv"
    )

    recommendations_cache["customer_id"] = (
        recommendations_cache["customer_id"].astype(str)
    )

    return recommendations_cache