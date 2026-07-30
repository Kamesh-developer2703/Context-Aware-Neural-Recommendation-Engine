import pandas as pd

RECOMMENDATION_FILE = "outputs/recommendations.csv"

def get_recommendations():

    df = pd.read_csv(RECOMMENDATION_FILE)

    return df.to_dict(orient="records")