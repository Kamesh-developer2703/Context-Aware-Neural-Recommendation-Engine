from fastapi import APIRouter, Query
from api.services import get_recommendations

router = APIRouter()

@router.get("/recommendations")
def recommendations(limit: int = Query(default=10, ge=1, le=100)):
    data = get_recommendations()

    return {
        "status": "success",
        "total": len(data[:limit]),
        "recommendations": data[:limit]
    }