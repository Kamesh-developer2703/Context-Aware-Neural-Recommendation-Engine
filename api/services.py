import pandas as pd
import os

FILE = "outputs/recommendations.csv"

def get_recommendations():

    if not os.path.exists(FILE):
        return []

    df = pd.read_csv(FILE)

    df = df.sort_values("score", ascending=False)

    return df.to_dict(orient="records")