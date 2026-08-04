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
def recommendation(customer_id: str):

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

@router.get("/statistics")
def statistics():

    import pandas as pd

    df = pd.read_csv("outputs/recommendations.csv")

    return {
        "total_recommendations": len(df),
        "unique_customers": int(df["customer_id"].nunique()),
        "unique_articles": int(df["article_id"].nunique()),
        "average_score": float(df["score"].mean()),
        "highest_score": float(df["score"].max())
    }