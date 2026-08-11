import os
import pandas as pd


FAVORITES_FILE = "outputs/favorites/customer_favorites.csv"
RECENT_FILE = "outputs/recent/customer_recent.csv"
FEEDBACK_FILE = "outputs/feedback/customer_feedback.csv"


def load_file(path, columns):

    if not os.path.exists(path):
        return pd.DataFrame(columns=columns)

    return pd.read_csv(path)


def get_trending(limit=10):

    # ---------------------------------
    # Load interaction data
    # ---------------------------------

    favorites = load_file(
        FAVORITES_FILE,
        ["customer_id", "article_id"]
    )

    recent = load_file(
        RECENT_FILE,
        ["customer_id", "article_id", "timestamp"]
    )

    feedback = load_file(
        FEEDBACK_FILE,
        [
            "customer_id",
            "article_id",
            "feedback",
            "timestamp"
        ]
    )

    # ---------------------------------
    # Calculate interaction scores
    # ---------------------------------

    scores = {}

    def add_score(article_id, value):

        article_id = int(article_id)

        scores[article_id] = (
            scores.get(article_id, 0) + value
        )

    # Favorite = +3
    for article_id in favorites["article_id"]:
        add_score(article_id, 3)

    # Recently viewed = +1
    for article_id in recent["article_id"]:
        add_score(article_id, 1)

    # Feedback
    for _, row in feedback.iterrows():

        article_id = row["article_id"]
        feedback_type = str(
            row["feedback"]
        ).lower()

        if feedback_type == "like":
            add_score(article_id, 4)

        elif feedback_type == "dislike":
            add_score(article_id, -3)

    # ---------------------------------
    # No interactions
    # ---------------------------------

    if not scores:

        return []

    # ---------------------------------
    # Create trending DataFrame
    # ---------------------------------

    trending = pd.DataFrame(
        [
            {
                "article_id": article_id,
                "score": score
            }
            for article_id, score
            in scores.items()
        ]
    )

    # Highest score first
    trending = trending.sort_values(
        by="score",
        ascending=False
    )

    # Limit results
    trending = trending.head(limit)

    return trending.to_dict(
        orient="records"
    )