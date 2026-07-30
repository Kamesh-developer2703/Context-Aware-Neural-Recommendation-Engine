from fastapi import APIRouter
from api.services import get_recommendations

router = APIRouter()

@router.get("/recommendations")
def recommendations():

    return {
        "status": "success",
        "total": len(get_recommendations()),
        "recommendations": get_recommendations()
    }