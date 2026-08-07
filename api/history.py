import os
import pandas as pd
from datetime import datetime

HISTORY_FILE = "outputs/history/recommendation_history.csv"

os.makedirs("outputs/history", exist_ok=True)


def save_history(customer_id, recommendations):

    if os.path.exists(HISTORY_FILE):
        history = pd.read_csv(HISTORY_FILE)
    else:
        history = pd.DataFrame(
            columns=[
                "customer_id",
                "article_id",
                "score",
                "timestamp"
            ]
        )

    timestamp = datetime.now()

    rows = []

    for item in recommendations:

        rows.append({
            "customer_id": customer_id,
            "article_id": item["article_id"],
            "score": item["score"],
            "timestamp": timestamp
        })

    history = pd.concat(
        [
            history,
            pd.DataFrame(rows)
        ],
        ignore_index=True
    )

    history.to_csv(
        HISTORY_FILE,
        index=False
    )