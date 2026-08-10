import os
import pandas as pd
from datetime import datetime

FEEDBACK_FILE = "outputs/feedback/customer_feedback.csv"

os.makedirs("outputs/feedback", exist_ok=True)


VALID_FEEDBACK = ["like", "dislike"]


def add_feedback(customer_id, article_id, feedback):

    customer_id = str(customer_id)
    article_id = int(article_id)
    feedback = str(feedback).lower()

    if feedback not in VALID_FEEDBACK:
        return {
            "status": "failed",
            "message": "Feedback must be 'like' or 'dislike'."
        }

    if os.path.exists(FEEDBACK_FILE):
        data = pd.read_csv(FEEDBACK_FILE)
    else:
        data = pd.DataFrame(
            columns=[
                "customer_id",
                "article_id",
                "feedback",
                "timestamp"
            ]
        )

    # Check existing feedback
    existing = (
        (data["customer_id"].astype(str) == customer_id)
        &
        (data["article_id"].astype(int) == article_id)
    )

    if existing.any():

        # Update existing feedback
        data.loc[existing, "feedback"] = feedback
        data.loc[existing, "timestamp"] = str(datetime.now())

        data.to_csv(
            FEEDBACK_FILE,
            index=False
        )

        return {
            "status": "success",
            "message": "Feedback updated successfully."
        }

    # Add new feedback
    new_row = pd.DataFrame([{
        "customer_id": customer_id,
        "article_id": article_id,
        "feedback": feedback,
        "timestamp": datetime.now()
    }])

    data = pd.concat(
        [data, new_row],
        ignore_index=True
    )

    data.to_csv(
        FEEDBACK_FILE,
        index=False
    )

    return {
        "status": "success",
        "message": "Feedback added successfully."
    }


def get_feedback(customer_id):

    if not os.path.exists(FEEDBACK_FILE):
        return []

    data = pd.read_csv(FEEDBACK_FILE)

    data["customer_id"] = (
        data["customer_id"].astype(str)
    )

    data = data[
        data["customer_id"] == str(customer_id)
    ]

    return data.to_dict(
        orient="records"
    )


def delete_feedback(customer_id, article_id):

    if not os.path.exists(FEEDBACK_FILE):

        return {
            "status": "failed",
            "message": "No feedback found."
        }

    data = pd.read_csv(FEEDBACK_FILE)

    customer_id = str(customer_id)
    article_id = int(article_id)

    existing = (
        (data["customer_id"].astype(str) == customer_id)
        &
        (data["article_id"].astype(int) == article_id)
    )

    if not existing.any():

        return {
            "status": "failed",
            "message": "Feedback not found."
        }

    data = data[~existing]

    data.to_csv(
        FEEDBACK_FILE,
        index=False
    )

    return {
        "status": "success",
        "message": "Feedback deleted successfully."
    }