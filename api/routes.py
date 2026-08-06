from fastapi import APIRouter, Query,HTTPException
from api.services import get_recommendations

router = APIRouter()

@router.get("/recommendations")
def recommendations(limit: int = Query(10, ge=1, le=100)):
    data = get_recommendations(customer_id)

    if len(data) == 0:
        raise HTTPException(
        status_code=404,
        detail=f"No recommendations found for customer_id={customer_id}"
    )

    return {
    "customer_id": customer_id,
    "total": len(data),
    "recommendations": data
}

@router.get("/recommendations/{customer_id}")
def customer_recommendations(customer_id: int):

    data = get_recommendations(customer_id)

    if len(data) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No recommendations found for customer_id={customer_id}"
        )

    return {
        "customer_id": customer_id,
        "total": len(data),
        "recommendations": data
    }