from fastapi import APIRouter, Query, HTTPException
from api.services import (
    get_recommendations,
    get_trending,
    get_personalized_recommendations,
    get_similar_articles
)
from api.schemas import FavoriteArticle, FavoriteResponse
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

# Temporary in-memory favorite articles store
_favorite_articles = set()
# Recently viewed articles per customer
_recently_viewed = {}

# Disliked articles per customer
_disliked_articles = {}

@router.get("/recommendations")
def recommendations(limit: int = Query(10, ge=1, le=100)):
    logger.info("Recommendation request received: limit=%s", limit)

    data = get_recommendations()

    if len(data) == 0:
        logger.warning("No recommendations available")
        raise HTTPException(
            status_code=404,
            detail="No recommendations found"
        )

    recommendations_data = data[:limit]

    logger.info(
        "Recommendation request completed: returned=%s",
        len(recommendations_data)
    )

    return {
        "status": "success",
        "total": len(recommendations_data),
        "recommendations": recommendations_data
    }


@router.get("/recommendations/{customer_id}")
def customer_recommendations(
    customer_id: int,
    limit: int = Query(10, ge=1, le=100)
):
    logger.info(
        "Customer recommendation request received: customer_id=%s, limit=%s",
        customer_id,
        limit
    )

    data = get_recommendations(customer_id)

    if len(data) == 0:
        logger.warning(
            "No recommendations found for customer_id=%s",
            customer_id
        )
        raise HTTPException(
            status_code=404,
            detail=f"No recommendations found for customer_id={customer_id}"
        )

    recommendations_data = data[:limit]

    logger.info(
        "Customer recommendation request completed: "
        "customer_id=%s, returned=%s",
        customer_id,
        len(recommendations_data)
    )

    return {
        "customer_id": customer_id,
        "total": len(recommendations_data),
        "recommendations": recommendations_data
    }
@router.get("/personalized/{customer_id}")
def personalized_recommendations(
    customer_id: int,
    limit: int = Query(10, ge=1, le=100)
):
    logger.info(
        "Personalized recommendation request: "
        "customer_id=%s, limit=%s",
        customer_id,
        limit
    )

    favorite_articles = _favorite_articles

    recently_viewed = _recently_viewed.get(
        customer_id,
        set()
    )

    disliked_articles = _disliked_articles.get(
        customer_id,
        set()
    )

    data = get_personalized_recommendations(
        customer_id=customer_id,
        limit=limit,
        favorite_articles=favorite_articles,
        recently_viewed=recently_viewed,
        disliked_articles=disliked_articles
    )

    if len(data) == 0:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No personalized recommendations found "
                f"for customer_id={customer_id}"
            )
        )

    return {
        "status": "success",
        "customer_id": customer_id,
        "total": len(data),
        "recommendations": data
    }
@router.post("/recently-viewed/{customer_id}/{article_id}")
def add_recently_viewed(
    customer_id: int,
    article_id: int
):
    if customer_id not in _recently_viewed:
        _recently_viewed[customer_id] = set()

    _recently_viewed[customer_id].add(article_id)

    logger.info(
        "Article marked as recently viewed: "
        "customer_id=%s, article_id=%s",
        customer_id,
        article_id
    )

    return {
        "status": "success",
        "customer_id": customer_id,
        "article_id": article_id
    }


@router.get("/recently-viewed/{customer_id}")
def get_recently_viewed(customer_id: int):
    articles = sorted(
        _recently_viewed.get(
            customer_id,
            set()
        )
    )

    return {
        "status": "success",
        "customer_id": customer_id,
        "total": len(articles),
        "recently_viewed": articles
    }
@router.post("/disliked/{customer_id}/{article_id}")
def add_disliked(
    customer_id: int,
    article_id: int
):
    if customer_id not in _disliked_articles:
        _disliked_articles[customer_id] = set()

    _disliked_articles[customer_id].add(article_id)

    logger.info(
        "Article disliked: "
        "customer_id=%s, article_id=%s",
        customer_id,
        article_id
    )

    return {
        "status": "success",
        "customer_id": customer_id,
        "article_id": article_id
    }


@router.get("/disliked/{customer_id}")
def get_disliked(customer_id: int):
    articles = sorted(
        _disliked_articles.get(
            customer_id,
            set()
        )
    )

    return {
        "status": "success",
        "customer_id": customer_id,
        "total": len(articles),
        "disliked": articles
    }
@router.post(
    "/favorites",
    response_model=FavoriteResponse
)
def add_favorite(article: FavoriteArticle):
    logger.info(
        "Favorite article request received: article_id=%s",
        article.article_id
    )

    if article.article_id in _favorite_articles:
        raise HTTPException(
            status_code=409,
            detail=f"Article {article.article_id} is already favorited."
        )

    _favorite_articles.add(article.article_id)

    logger.info(
        "Article favorited successfully: article_id=%s",
        article.article_id
    )

    return FavoriteResponse(
        status="success",
        article_id=article.article_id
    )

# -----------------------------
# Trending Articles API
# -----------------------------

@router.get("/trending")
def trending(
    limit: int = Query(10, ge=1, le=100)
):
    logger.info(
        "Trending request received: limit=%s",
        limit
    )

    data = get_trending(limit)

    logger.info(
        "Trending request completed: returned=%s",
        len(data)
    )

    return {
        "status": "success",
        "total": len(data),
        "trending": data
    }
# -----------------------------
# Similar Articles API
# -----------------------------

@router.get("/similar/{article_id}")
def similar_articles(
    article_id: int,
    limit: int = Query(10, ge=1, le=100),
):
    logger.info(
        "Similar articles request received: "
        "article_id=%s, limit=%s",
        article_id,
        limit,
    )

    data = get_similar_articles(
        article_id,
        limit,
    )

    if data is None:
        logger.warning(
            "Article not found: article_id=%s",
            article_id,
        )
        raise HTTPException(
            status_code=404,
            detail=f"Article {article_id} not found.",
        )

    logger.info(
        "Similar articles request completed: "
        "article_id=%s, returned=%s",
        article_id,
        len(data),
    )

    return {
        "status": "success",
        "article_id": article_id,
        "total": len(data),
        "similar_articles": data,
    }

@router.get("/favorites")
def get_favorites():
    logger.info("Favorite articles request received")

    favorites = sorted(_favorite_articles)

    return {
        "status": "success",
        "total": len(favorites),
        "favorites": favorites
    }


@router.delete(
    "/favorites/{article_id}",
    response_model=FavoriteResponse
)
def remove_favorite(article_id: int):
    logger.info(
        "Remove favorite request received: article_id=%s",
        article_id
    )

    if article_id not in _favorite_articles:
        raise HTTPException(
            status_code=404,
            detail=f"Article {article_id} is not favorited."
        )

    _favorite_articles.remove(article_id)

    logger.info(
        "Article removed from favorites: article_id=%s",
        article_id
    )

    return FavoriteResponse(
        status="success",
        article_id=article_id
    )