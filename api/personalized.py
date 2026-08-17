import os
import pandas as pd

from ann.recommender import get_dynamic_recommendations


# ============================================================
# File locations
# ============================================================

FAVORITES_FILE = "outputs/favorites/customer_favorites.csv"
RECENT_FILE = "outputs/recent/customer_recent.csv"
FEEDBACK_FILE = "outputs/feedback/customer_feedback.csv"


# ============================================================
# CSV Loader
# ============================================================

def load_csv(path, columns):

    if not os.path.exists(path):
        return pd.DataFrame(columns=columns)

    try:
        df = pd.read_csv(path)
    except Exception:
        return pd.DataFrame(columns=columns)

    # Make sure expected columns exist
    for column in columns:
        if column not in df.columns:
            df[column] = None

    return df


# ============================================================
# Personalized Recommendation Engine
# ============================================================

def get_personalized_recommendations(
    customer_id,
    limit=10
):

    customer_id = str(customer_id)

    # --------------------------------------------------------
    # Validate limit
    # --------------------------------------------------------

    if limit < 1:
        return []

    # --------------------------------------------------------
    # STEP 1
    # Get recommendations from Two-Tower model
    # --------------------------------------------------------

    try:

        dynamic_recommendations = (
            get_dynamic_recommendations(
                customer_id,
                limit=100
            )
        )

    except Exception as e:

        print(
            f"Error generating recommendations: {e}"
        )

        return []

    if not dynamic_recommendations:
        return []

    recommendations = pd.DataFrame(
        dynamic_recommendations
    )

    if recommendations.empty:
        return []

    # --------------------------------------------------------
    # Validate required columns
    # --------------------------------------------------------

    required_columns = [
        "article_id",
        "score"
    ]

    for column in required_columns:

        if column not in recommendations.columns:
            return []

    # --------------------------------------------------------
    # Normalize data types
    # --------------------------------------------------------

    recommendations["article_id"] = pd.to_numeric(
        recommendations["article_id"],
        errors="coerce"
    )

    recommendations["score"] = pd.to_numeric(
        recommendations["score"],
        errors="coerce"
    )

    recommendations = recommendations.dropna(
        subset=["article_id", "score"]
    )

    recommendations["article_id"] = (
        recommendations["article_id"].astype(int)
    )

    recommendations["score"] = (
        recommendations["score"].astype(float)
    )

    # --------------------------------------------------------
    # STEP 2
    # Load user interaction data
    # --------------------------------------------------------

    favorites = load_csv(
        FAVORITES_FILE,
        [
            "customer_id",
            "article_id"
        ]
    )

    recent = load_csv(
        RECENT_FILE,
        [
            "customer_id",
            "article_id",
            "timestamp"
        ]
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

    # ========================================================
    # STEP 3
    # Get user's favorite articles
    # ========================================================

    favorite_articles = set()

    if not favorites.empty:

        favorites["customer_id"] = (
            favorites["customer_id"].astype(str)
        )

        user_favorites = favorites[
            favorites["customer_id"] == customer_id
        ]

        if not user_favorites.empty:

            favorite_ids = pd.to_numeric(
                user_favorites["article_id"],
                errors="coerce"
            ).dropna()

            favorite_articles = set(
                favorite_ids.astype(int)
            )

    # ========================================================
    # STEP 4
    # Get recently viewed articles
    # ========================================================

    recent_articles = set()

    if not recent.empty:

        recent["customer_id"] = (
            recent["customer_id"].astype(str)
        )

        user_recent = recent[
            recent["customer_id"] == customer_id
        ]

        if not user_recent.empty:

            recent_ids = pd.to_numeric(
                user_recent["article_id"],
                errors="coerce"
            ).dropna()

            recent_articles = set(
                recent_ids.astype(int)
            )

    # ========================================================
    # STEP 5
    # Get user feedback
    # ========================================================

    feedback_map = {}

    if not feedback.empty:

        feedback["customer_id"] = (
            feedback["customer_id"].astype(str)
        )

        user_feedback = feedback[
            feedback["customer_id"] == customer_id
        ]

        for _, row in user_feedback.iterrows():

            article_id = pd.to_numeric(
                row["article_id"],
                errors="coerce"
            )

            if pd.isna(article_id):
                continue

            feedback_value = str(
                row["feedback"]
            ).strip().lower()

            feedback_map[
                int(article_id)
            ] = feedback_value

    # ========================================================
    # STEP 6
    # Calculate personalized score
    # ========================================================

    def calculate_score(row):

        article_id = int(
            row["article_id"]
        )

        base_score = float(
            row["score"]
        )

        final_score = base_score

        # --------------------------------------------
        # Favorite boost
        # --------------------------------------------

        if article_id in favorite_articles:

            final_score += 3.0

        # --------------------------------------------
        # Recently viewed boost
        # --------------------------------------------

        if article_id in recent_articles:

            final_score += 1.0

        # --------------------------------------------
        # Feedback
        # --------------------------------------------

        feedback_value = feedback_map.get(
            article_id
        )

        if feedback_value == "like":

            final_score += 4.0

        elif feedback_value == "dislike":

            final_score -= 3.0

        return final_score

    # --------------------------------------------------------
    # Apply personalization
    # --------------------------------------------------------

    recommendations["final_score"] = (
        recommendations.apply(
            calculate_score,
            axis=1
        )
    )

    # ========================================================
    # STEP 7
    # Remove disliked / invalid recommendations
    # ========================================================

    recommendations = recommendations[
        recommendations["final_score"] > 0
    ]

    if recommendations.empty:
        return []

    # ========================================================
    # STEP 8
    # Sort by personalized score
    # ========================================================

    recommendations = recommendations.sort_values(
        by="final_score",
        ascending=False
    )

    # --------------------------------------------------------
    # Remove duplicate articles
    # --------------------------------------------------------

    recommendations = recommendations.drop_duplicates(
        subset=["article_id"]
    )

    # --------------------------------------------------------
    # Take Top-K
    # --------------------------------------------------------

    recommendations = recommendations.head(
        limit
    )

    # ========================================================
    # STEP 9
    # Build API response
    # ========================================================

    results = []

    for _, row in recommendations.iterrows():

        results.append({

            "article_id": int(
                row["article_id"]
            ),

            "score": round(
                float(row["final_score"]),
                6
            )
        })

    return results