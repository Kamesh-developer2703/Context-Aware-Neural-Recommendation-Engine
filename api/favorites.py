import os
import pandas as pd

FAVORITE_FILE = "outputs/favorites/customer_favorites.csv"

os.makedirs("outputs/favorites", exist_ok=True)


def add_favorite(customer_id, article_id):

    if os.path.exists(FAVORITE_FILE):
        favorites = pd.read_csv(FAVORITE_FILE)
    else:
        favorites = pd.DataFrame(
            columns=["customer_id", "article_id"]
        )

    customer_id = str(customer_id)
    article_id = int(article_id)

    exists = (
        (favorites["customer_id"].astype(str) == customer_id) &
        (favorites["article_id"] == article_id)
    ).any()

    if not exists:

        favorites.loc[len(favorites)] = [
            customer_id,
            article_id
        ]

        favorites.to_csv(
            FAVORITE_FILE,
            index=False
        )

        return {
            "status": "success",
            "message": "Article added to favorites."
        }

    return {
        "status": "success",
        "message": "Article already exists in favorites."
    }


def get_favorites(customer_id):

    if not os.path.exists(FAVORITE_FILE):
        return []

    favorites = pd.read_csv(FAVORITE_FILE)

    favorites["customer_id"] = (
        favorites["customer_id"].astype(str)
    )

    favorites = favorites[
        favorites["customer_id"] == str(customer_id)
    ]

    return favorites.to_dict(
        orient="records"
    )


def remove_favorite(customer_id, article_id):

    if not os.path.exists(FAVORITE_FILE):

        return {
            "status": "failed",
            "message": "No favorites found."
        }

    favorites = pd.read_csv(FAVORITE_FILE)

    favorites = favorites[
        ~(
            (favorites["customer_id"].astype(str) == str(customer_id))
            &
            (favorites["article_id"] == int(article_id))
        )
    ]

    favorites.to_csv(
        FAVORITE_FILE,
        index=False
    )

    return {
        "status": "success",
        "message": "Favorite removed successfully."
    }