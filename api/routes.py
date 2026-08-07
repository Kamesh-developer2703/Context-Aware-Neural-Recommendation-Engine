from fastapi import APIRouter, Query, HTTPException
from api.services import get_recommendations
import logging

router = APIRouter()

logger = logging.getLogger(__name__)


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
def customer_recommendations(customer_id: int):
    logger.info(
        "Customer recommendation request received: customer_id=%s",
        customer_id
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

    logger.info(
        "Customer recommendation request completed: customer_id=%s, returned=%s",
        customer_id,
        len(data)
    )

    return {
        "customer_id": customer_id,
        "total": len(data),
        "recommendations": data
    }