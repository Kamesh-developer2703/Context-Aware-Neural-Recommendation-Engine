from fastapi import APIRouter, HTTPException, Query

from api.services import get_recommendations

router = APIRouter()

@router.get("/recommendations")
def recommendations(limit: int = Query(10, ge=1, le=100)):

    try:

        data = get_recommendations()

        return {
            "status":"success",
            "total":len(data[:limit]),
            "recommendations":data[:limit]
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get("/recommendations/{customer_id}")
def recommendation(customer_id:int):

    data = get_recommendations(customer_id)

    if len(data)==0:

        raise HTTPException(
            status_code=404,
            detail="Customer recommendation not found."
        )

    return {
        "customer_id":customer_id,
        "recommendations":data
    }