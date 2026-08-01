import os
import pandas as pd

FILE = "outputs/recommendations.csv"

def get_recommendations(customer_id=None):

    if not os.path.exists(FILE):
        return []

    df = pd.read_csv(FILE)

    # If customer_id column exists, filter recommendations
    if customer_id is not None and "customer_id" in df.columns:
        df = df[df["customer_id"] == customer_id]

    df = df.sort_values("score", ascending=False)

    return df.to_dict(orient="records")     