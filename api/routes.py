from fastapi import APIRouter, HTTPException, Query

from api.services import get_recommendations

from utils.logger import log_request

from api.cache import refresh_cache

from api.history import save_history

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

    save_history(
    customer_id,
    data
)

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

    log_request(
        "/recommendations",
        customer_id,
        "SUCCESS"
    )

    return {
        "customer_id": customer_id,
        "recommendations": data
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

@router.get("/logs")
def view_logs():

    import pandas as pd

    try:

        logs = pd.read_csv("outputs/logs/api_requests.csv")

        return logs.to_dict(orient="records")

    except FileNotFoundError:

        return {
            "message": "No logs available."
        }

@router.post("/refresh-cache")
def reload_cache():

    refresh_cache()

    return {
        "status": "success",
        "message": "Recommendation cache refreshed."
    }

@router.get("/history")
def recommendation_history():

    import pandas as pd

    try:

        history = pd.read_csv(
            "outputs/history/recommendation_history.csv"
        )

        return {
            "total": len(history),
            "history": history.to_dict(
                orient="records"
            )
        }

    except FileNotFoundError:

        return {
            "message": "No history available."
        }

@router.get("/history/{customer_id}")
def customer_history(customer_id: str):

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
            "history": history.to_dict(
                orient="records"
            )
        }

    except FileNotFoundError:

        return {
            "message": "No history found."
        }