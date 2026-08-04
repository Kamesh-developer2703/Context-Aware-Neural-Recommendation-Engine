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
def get_customer_recommendations(customer_id: str, limit: int = 10):
    # Sample mock candidates for API testing/demo
    sample_items = [
        {"article_id": "0108775015", "score": 0.985, "product_type": "Dress"},
        {"article_id": "0108775016", "score": 0.942, "product_type": "Trousers"},
        {"article_id": "0108775017", "score": 0.891, "product_type": "Jacket"},
        {"article_id": "0108775018", "score": 0.854, "product_type": "Sweater"},
        {"article_id": "0108775019", "score": 0.812, "product_type": "Top"}
    ]
    
    return {
        "customer_id": customer_id,
        "total": len(sample_items[:limit]),
        "recommendations": sample_items[:limit]
    }