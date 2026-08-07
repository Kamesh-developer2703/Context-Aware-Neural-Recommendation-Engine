import math
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, status
from api.schemas import (
    RecommendationResponse, 
    RecommendationItem, 
    PaginatedHistoryResponse, 
    HistoryRecord
)

router = APIRouter()

# --- MOCK DATA STORES ---
CANDIDATE_UNIVERSE = [
    {"article_id": "0108775015", "score": 0.985, "product_type": "Dress", "product_group_name": "Garments"},
    {"article_id": "0108775016", "score": 0.942, "product_type": "Trousers", "product_group_name": "Garments"},
    {"article_id": "0108775017", "score": 0.891, "product_type": "Jacket", "product_group_name": "Garments"},
    {"article_id": "0108775018", "score": 0.854, "product_type": "Sweater", "product_group_name": "Garments"},
    {"article_id": "0108775019", "score": 0.812, "product_type": "Top", "product_group_name": "Garments"},
    {"article_id": "0108775020", "score": 0.765, "product_type": "Sports Shoes", "product_group_name": "Footwear"},
    {"article_id": "0108775021", "score": 0.690, "product_type": "Running Shorts", "product_group_name": "Sportswear"},
    {"article_id": "0108775022", "score": 0.550, "product_type": "Cap", "product_group_name": "Accessories"},
]

RECOMMENDATION_HISTORY_STORE = [
    {
        "recommendation_id": "REC_1001",
        "customer_id": "CUST_10",
        "timestamp": "2026-08-07 14:20:00",
        "items_recommended": [
            {"article_id": "0108775015", "score": 0.985, "product_type": "Dress", "product_group_name": "Garments"},
            {"article_id": "0108775016", "score": 0.942, "product_type": "Trousers", "product_group_name": "Garments"}
        ]
    },
    {
        "recommendation_id": "REC_1002",
        "customer_id": "CUST_10",
        "timestamp": "2026-08-06 11:15:00",
        "items_recommended": [
            {"article_id": "0108775017", "score": 0.891, "product_type": "Jacket", "product_group_name": "Garments"}
        ]
    },
    {
        "recommendation_id": "REC_1003",
        "customer_id": "CUST_20",
        "timestamp": "2026-08-05 09:30:00",
        "items_recommended": [
            {"article_id": "0108775020", "score": 0.765, "product_type": "Sports Shoes", "product_group_name": "Footwear"}
        ]
    }
]


# --- 1. GENERAL & CUSTOMER RECOMMENDATIONS ENDPOINTS ---
@router.get(
    "/recommendations/{customer_id}",
    response_model=RecommendationResponse,
    summary="Get Customer Specific Recommendations"
)
def get_customer_recommendations(customer_id: str, limit: int = Query(10, ge=1, le=100)):
    try:
        recs = CANDIDATE_UNIVERSE[:limit]
        return RecommendationResponse(
            status="success",
            customer_id=customer_id,
            total_found=len(recs),
            returned_count=len(recs),
            recommendations=[RecommendationItem(**item) for item in recs]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )


# --- 2. SEARCH & FILTER RECOMMENDATIONS ENDPOINT ---
@router.get(
    "/recommendations/search",
    response_model=RecommendationResponse,
    summary="Search and Filter Recommendations"
)
def search_and_filter_recommendations(
    customer_id: Optional[str] = Query(None, description="Customer ID"),
    query: Optional[str] = Query(None, description="Search term"),
    min_score: float = Query(0.0, ge=0.0, le=1.0, description="Minimum score threshold"),
    top_k: int = Query(10, ge=1, le=100, description="Limit results")
):
    try:
        results = CANDIDATE_UNIVERSE.copy()

        if query:
            q_clean = query.strip().lower()
            results = [
                item for item in results 
                if q_clean in item["product_type"].lower() or q_clean in item["article_id"].lower()
            ]

        results = [item for item in results if item["score"] >= min_score]
        results.sort(key=lambda x: x["score"], reverse=True)
        final_recs = results[:top_k]

        return RecommendationResponse(
            status="success",
            customer_id=customer_id,
            search_query=query,
            min_score_filter=min_score,
            total_found=len(results),
            returned_count=len(final_recs),
            recommendations=[RecommendationItem(**item) for item in final_recs]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error filtering recommendations: {str(e)}"
        )


# --- 3. PAGINATED HISTORY ENDPOINT ---
@router.get(
    "/recommendations/history",
    response_model=PaginatedHistoryResponse,
    summary="Get Paginated Recommendation History"
)
def get_recommendation_history(
    customer_id: Optional[str] = Query(None, description="Filter history by Customer ID"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
):
    try:
        filtered_history = RECOMMENDATION_HISTORY_STORE.copy()

        if customer_id:
            c_clean = customer_id.strip().upper()
            filtered_history = [
                rec for rec in filtered_history 
                if c_clean in rec["customer_id"].upper()
            ]

        total_records = len(filtered_history)
        if total_records == 0:
            return PaginatedHistoryResponse(
                status="success",
                customer_id=customer_id,
                page=page,
                limit=limit,
                total_records=0,
                total_pages=0,
                has_next=False,
                has_prev=False,
                history=[]
            )

        total_pages = math.ceil(total_records / limit)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_records = filtered_history[start_idx:end_idx]

        return PaginatedHistoryResponse(
            status="success",
            customer_id=customer_id,
            page=page,
            limit=limit,
            total_records=total_records,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
            history=[HistoryRecord(**rec) for rec in paginated_records]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving history: {str(e)}"
        )