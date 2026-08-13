import os
import pandas as pd


RECOMMENDATION_FILE = "outputs/recommendations.csv"
FAVORITES_FILE = "outputs/favorites/customer_favorites.csv"
RECENT_FILE = "outputs/recent/customer_recent.csv"
FEEDBACK_FILE = "outputs/feedback/customer_feedback.csv"


def load_csv(path, columns):

    if not os.path.exists(path):
        return pd.DataFrame(columns=columns)

    return pd.read_csv(path)


def get_personalized_recommendations(customer_id, limit=10):

    customer_id = str(customer_id)

    # ---------------------------------------
    # Load base recommendations
    # ---------------------------------------

    recommendations = load_csv(
        RECOMMENDATION_FILE,
        ["customer_id", "article_id", "score"]
    )

    if recommendations.empty:
        return []

    recommendations["customer_id"] = (
        recommendations["customer_id"].astype(str)
    )

    recommendations = recommendations[
        recommendations["customer_id"] == customer_id
    ].copy()

    if recommendations.empty:
        return []

    # ---------------------------------------
    # Load user interactions
    # ---------------------------------------

    favorites = load_csv(
        FAVORITES_FILE,
        ["customer_id", "article_id"]
    )

    recent = load_csv(
        RECENT_FILE,
        ["customer_id", "article_id", "timestamp"]
    )

    feedback = load_csv(
        FEEDBACK_FILE,
        [
            "customer_id",
            "article_id",
            "feedback",
            "timestamp"
        ]
    )

    # ---------------------------------------
    # Convert article IDs
    # ---------------------------------------

    recommendations["article_id"] = (
        recommendations["article_id"].astype(int)
    )

    # ---------------------------------------
    # Interaction sets
    # ---------------------------------------

    favorite_articles = set()

    if not favorites.empty:

        favorites["customer_id"] = (
            favorites["customer_id"].astype(str)
        )

        favorite_articles = set(
            favorites[
                favorites["customer_id"] == customer_id
            ]["article_id"].astype(int)
        )

    recent_articles = set()

    if not recent.empty:

        recent["customer_id"] = (
            recent["customer_id"].astype(str)
        )

        recent_articles = set(
            recent[
                recent["customer_id"] == customer_id
            ]["article_id"].astype(int)
        )

    # ---------------------------------------
    # Feedback mapping
    # ---------------------------------------

    feedback_map = {}

    if not feedback.empty:

        feedback["customer_id"] = (
            feedback["customer_id"].astype(str)
        )

        user_feedback = feedback[
            feedback["customer_id"] == customer_id
        ]

        for _, row in user_feedback.iterrows():

            feedback_map[
                int(row["article_id"])
            ] = str(
                row["feedback"]
            ).lower()

    # ---------------------------------------
    # Calculate final score
    # ---------------------------------------

    def calculate_score(row):

        article_id = int(row["article_id"])

        base_score = float(row["score"])

        final_score = base_score

        # Favorite boost
        if article_id in favorite_articles:
            final_score += 3.0

        # Recently viewed boost
        if article_id in recent_articles:
            final_score += 1.0

        # Feedback
        feedback_value = feedback_map.get(
            article_id
        )

        if feedback_value == "like":
            final_score += 4.0

        elif feedback_value == "dislike":
            final_score -= 3.0

        return final_score

    recommendations["final_score"] = (
        recommendations.apply(
            calculate_score,
            axis=1
        )
    )

    # ---------------------------------------
    # Remove disliked recommendations
    # ---------------------------------------

    recommendations = recommendations[
        recommendations["final_score"] > 0
    ]

    # ---------------------------------------
    # Sort by final score
    # ---------------------------------------

    recommendations = recommendations.sort_values(
        by="final_score",
        ascending=False
    )

    recommendations = recommendations.head(
        limit
    )

    # ---------------------------------------
    # Response
    # ---------------------------------------

    results = []

    for _, row in recommendations.iterrows():

        results.append({
            "article_id": int(row["article_id"]),
            "score": round(
                float(row["final_score"]),
                6
            )
        })

    return results