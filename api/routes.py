from fastapi import APIRouter, Query
from api.services import get_recommendations

router = APIRouter()

@router.get("/recommendations")
def recommendations(limit: int = Query(10, ge=1, le=100)):
    data = get_recommendations()

    return {
        "status": "success",
        "total": len(data[:limit]),
        "recommendations": data[:limit]
    }

@router.get("/recommendations/{customer_id}")
def customer_recommendations(customer_id: int):

    data = get_recommendations(customer_id)

    return {
        "customer_id": customer_id,
        "total": len(data),
        "recommendations": data
    }