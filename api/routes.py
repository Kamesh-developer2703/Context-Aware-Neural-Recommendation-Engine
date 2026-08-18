from fastapi import APIRouter, HTTPException, Query

from api.services import get_recommendations
from utils.logger import log_request
from api.cache import refresh_cache
from api.history import save_history
from api.trending import get_trending
from api.similar import get_similar_articles

from api.favorites import (
    add_favorite,
    get_favorites,
    remove_favorite
)

from api.recent import (
    add_recent,
    get_recent,
    remove_recent
)

from api.feedback import (
    add_feedback,
    get_feedback,
    delete_feedback
)

from api.personalized import (
    get_personalized_recommendations
)


router = APIRouter()


# ============================================================
# GLOBAL RECOMMENDATIONS
# ============================================================

@router.get("/recommendations")
def recommendations(
    limit: int = Query(10, ge=1, le=100)
):

    try:

        data = get_recommendations()

        return {
            "status": "success",
            "total": len(data[:limit]),
            "recommendations": data[:limit]
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# ============================================================
# CUSTOMER RECOMMENDATIONS
# ============================================================

@router.get("/recommendations/{customer_id}")
def recommendation(
    customer_id: str,
    limit: int = Query(10, ge=1, le=100)
):

    data = get_recommendations(
        customer_id,
        limit
    )

    # Customer not found
    if len(data) == 0:

        log_request(
            "/recommendations",
            customer_id,
            "NOT FOUND"
        )

        raise HTTPException(
            status_code=404,
            detail="Customer recommendation not found."
        )

    # --------------------------------------------------------
    # Save recommendation history
    # --------------------------------------------------------

    save_history(
        customer_id,
        data
    )

    # --------------------------------------------------------
    # Log request
    # --------------------------------------------------------

    log_request(
        "/recommendations",
        customer_id,
        "SUCCESS"
    )

    return {
        "customer_id": customer_id,
        "total": len(data),
        "recommendations": data
    }


# ============================================================
# STATISTICS
# ============================================================

@router.get("/statistics")
def statistics():

    import pandas as pd

    try:

        df = pd.read_csv(
            "outputs/recommendations.csv"
        )

        return {
            "status": "success",
            "total_recommendations": len(df),
            "unique_customers": int(
                df["customer_id"].nunique()
            ),
            "unique_articles": int(
                df["article_id"].nunique()
            ),
            "average_score": float(
                df["score"].mean()
            ),
            "highest_score": float(
                df["score"].max()
            )
        }

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Recommendation file not found."
        )


# ============================================================
# API LOGS
# ============================================================

@router.get("/logs")
def view_logs():

    import pandas as pd

    try:

        logs = pd.read_csv(
            "outputs/logs/api_requests.csv"
        )

        return logs.to_dict(
            orient="records"
        )

    except FileNotFoundError:

        return {
            "message": "No logs available."
        }


# ============================================================
# REFRESH RECOMMENDATION CACHE
# ============================================================

@router.post("/refresh-cache")
def reload_cache():

    refresh_cache()

    return {
        "status": "success",
        "message": "Recommendation cache refreshed."
    }


# ============================================================
# ALL RECOMMENDATION HISTORY
# ============================================================

@router.get("/history")
def recommendation_history():

    import pandas as pd

    try:

        history = pd.read_csv(
            "outputs/history/recommendation_history.csv"
        )

        return {
            "status": "success",
            "total": len(history),
            "history": history.to_dict(
                orient="records"
            )
        }

    except FileNotFoundError:

        return {
            "status": "success",
            "total": 0,
            "history": []
        }


# ============================================================
# CUSTOMER RECOMMENDATION HISTORY
# ============================================================

@router.get("/history/{customer_id}")
def customer_history(
    customer_id: str
):

    import pandas as pd

    try:

        history = pd.read_csv(
            "outputs/history/recommendation_history.csv"
        )

        history["customer_id"] = (
            history["customer_id"].astype(str)
        )

        history = history[
            history["customer_id"] == customer_id
        ]

        return {
            "customer_id": customer_id,
            "total": len(history),
            "history": history.to_dict(
                orient="records"
            )
        }

    except FileNotFoundError:

        return {
            "customer_id": customer_id,
            "total": 0,
            "history": []
        }


# ============================================================
# FAVORITES
# ============================================================

@router.post(
    "/favorites/{customer_id}/{article_id}"
)
def favorite_article(
    customer_id: str,
    article_id: int
):

    return add_favorite(
        customer_id,
        article_id
    )


@router.get(
    "/favorites/{customer_id}"
)
def view_favorites(
    customer_id: str
):

    favorites = get_favorites(
        customer_id
    )

    return {
        "customer_id": customer_id,
        "total": len(favorites),
        "favorites": favorites
    }


@router.delete(
    "/favorites/{customer_id}/{article_id}"
)
def delete_favorite(
    customer_id: str,
    article_id: int
):

    return remove_favorite(
        customer_id,
        article_id
    )


# ============================================================
# RECENTLY VIEWED
# ============================================================

@router.post(
    "/recent/{customer_id}/{article_id}"
)
def add_recent_article(
    customer_id: str,
    article_id: int
):

    return add_recent(
        customer_id,
        article_id
    )


@router.get(
    "/recent/{customer_id}"
)
def view_recent_articles(
    customer_id: str,
    limit: int = Query(
        10,
        ge=1,
        le=100
    )
):

    recent = get_recent(
        customer_id,
        limit
    )

    return {
        "customer_id": customer_id,
        "total": len(recent),
        "recent": recent
    }


@router.delete(
    "/recent/{customer_id}/{article_id}"
)
def delete_recent_article(
    customer_id: str,
    article_id: int
):

    return remove_recent(
        customer_id,
        article_id
    )


# ============================================================
# FEEDBACK
# ============================================================

@router.post(
    "/feedback/{customer_id}/{article_id}"
)
def submit_feedback(
    customer_id: str,
    article_id: int,
    feedback: str
):

    return add_feedback(
        customer_id,
        article_id,
        feedback
    )


@router.get(
    "/feedback/{customer_id}"
)
def view_feedback(
    customer_id: str
):

    feedback = get_feedback(
        customer_id
    )

    return {
        "customer_id": customer_id,
        "total": len(feedback),
        "feedback": feedback
    }


@router.delete(
    "/feedback/{customer_id}/{article_id}"
)
def remove_feedback(
    customer_id: str,
    article_id: int
):

    return delete_feedback(
        customer_id,
        article_id
    )


# ============================================================
# TRENDING ARTICLES
# ============================================================

@router.get("/trending")
def trending_articles(
    limit: int = Query(
        10,
        ge=1,
        le=100
    )
):

    trending = get_trending(
        limit
    )

    return {
        "status": "success",
        "total": len(trending),
        "trending": trending
    }


# ============================================================
# SIMILAR ARTICLES
# ============================================================

@router.get("/similar/{article_id}")
def similar_articles(
    article_id: int,
    limit: int = Query(
        10,
        ge=1,
        le=100
    )
):

    results = get_similar_articles(
        article_id,
        limit
    )

    if results is None:

        raise HTTPException(
            status_code=404,
            detail="Article not found."
        )

    return {
        "status": "success",
        "article_id": article_id,
        "total": len(results),
        "similar": results
    }


# ============================================================
# PERSONALIZED RECOMMENDATIONS
# ============================================================

@router.get(
    "/personalized/{customer_id}"
)
def personalized_recommendations(
    customer_id: str,
    limit: int = Query(
        10,
        ge=1,
        le=100
    )
):

    recommendations = (
        get_personalized_recommendations(
            customer_id,
            limit
        )
    )

    if not recommendations:

        raise HTTPException(
            status_code=404,
            detail="No personalized recommendations found."
        )

    return {
        "status": "success",
        "customer_id": customer_id,
        "total": len(recommendations),
        "recommendations": recommendations
    }