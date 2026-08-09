import os
import pandas as pd
from datetime import datetime

RECENT_FILE = "outputs/recent/customer_recent.csv"

os.makedirs("outputs/recent", exist_ok=True)


def add_recent(customer_id, article_id):

    customer_id = str(customer_id)
    article_id = int(article_id)

    if os.path.exists(RECENT_FILE):
        recent = pd.read_csv(RECENT_FILE)
    else:
        recent = pd.DataFrame(
            columns=[
                "customer_id",
                "article_id",
                "timestamp"
            ]
        )

    # Remove existing entry for the same customer/article
    recent = recent[
        ~(
            (recent["customer_id"].astype(str) == customer_id)
            &
            (recent["article_id"].astype(int) == article_id)
        )
    ]

    # Add latest view
    new_row = pd.DataFrame([{
        "customer_id": customer_id,
        "article_id": article_id,
        "timestamp": datetime.now()
    }])

    recent = pd.concat(
        [recent, new_row],
        ignore_index=True
    )

    recent.to_csv(
        RECENT_FILE,
        index=False
    )

    return {
        "status": "success",
        "message": "Article added to recently viewed."
    }


def get_recent(customer_id, limit=10):

    if not os.path.exists(RECENT_FILE):
        return []

    recent = pd.read_csv(RECENT_FILE)

    recent["customer_id"] = (
        recent["customer_id"].astype(str)
    )

    recent = recent[
        recent["customer_id"] == str(customer_id)
    ]

    # Latest viewed articles first
    recent = recent.sort_values(
        by="timestamp",
        ascending=False
    )

    recent = recent.head(limit)

    return recent.to_dict(
        orient="records"
    )


def remove_recent(customer_id, article_id):

    if not os.path.exists(RECENT_FILE):
        return {
            "status": "failed",
            "message": "No recently viewed data found."
        }

    recent = pd.read_csv(RECENT_FILE)

    recent = recent[
        ~(
            (recent["customer_id"].astype(str) == str(customer_id))
            &
            (recent["article_id"].astype(int) == int(article_id))
        )
    ]

    recent.to_csv(
        RECENT_FILE,
        index=False
    )

    return {
        "status": "success",
        "message": "Article removed from recently viewed."
    }