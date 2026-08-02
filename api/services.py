import os
import pandas as pd

FILE = "outputs/recommendations.csv"

def get_recommendations(customer_id=None):

    if not os.path.exists(FILE):
        raise FileNotFoundError("Recommendation file not found.")

    df = pd.read_csv(FILE)

    if df.empty:
        return []

    if customer_id is not None:

        if "customer_id" not in df.columns:
            return []

        df = df[df["customer_id"] == customer_id]

    df = df.sort_values("score", ascending=False)

    return df.to_dict(orient="records")