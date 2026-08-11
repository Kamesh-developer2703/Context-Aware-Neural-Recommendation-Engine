import math
from typing import Optional, List
from fastapi import APIRouter, Query, Path, HTTPException, status
from api.schemas import (
    RecommendationResponse, 
    RecommendationItem, 
    PaginatedHistoryResponse, 
    HistoryRecord,
    CustomerProfileResponse,
    CustomerProfile,
    AggregatedCustomerActivityResponse,
    CustomerActivityTreeData,
    InteractionArticle,
    FeedbackItem
)

router = APIRouter()

# =====================================================================
# 📦 MOCK DATA STORES
# =====================================================================

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

CUSTOMER_PROFILES_STORE = {
    "CUST_10": {
        "customer_id": "CUST_10",
        "name": "Mokshitha",
        "email": "mokshitha@example.com",
        "membership_status": "Gold",
        "age_group": "20-29",
        "total_purchases": 28,
        "preferences": {
            "preferred_categories": ["Dresses", "Trousers", "Jackets"],
            "frequent_sizes": ["M", "S"],
            "favorite_colors": ["Black", "Blue", "White"]
        }
    },
    "CUST_20": {
        "customer_id": "CUST_20",
        "name": "Alex Smith",
        "email": "alex.smith@example.com",
        "membership_status": "Silver",
        "age_group": "30-39",
        "total_purchases": 12,
        "preferences": {
            "preferred_categories": ["Footwear", "Sportswear"],
            "frequent_sizes": ["L", "42"],
            "favorite_colors": ["Red", "Grey"]
        }
    }
}

CUSTOMER_ACTIVITY_STORE = {
    "CUST_10": {
        "recently_viewed": [
            {"article_id": "0108775015", "product_type": "Dress", "product_group_name": "Garments", "interacted_at": "2026-08-10 18:30:00"},
            {"article_id": "0108775016", "product_type": "Trousers", "product_group_name": "Garments", "interacted_at": "2026-08-09 10:15:00"}
        ],
        "favorites": [
            {"article_id": "0108775015", "product_type": "Dress", "product_group_name": "Garments", "interacted_at": "2026-08-07 12:00:00"},
            {"article_id": "0108775017", "product_type": "Jacket", "product_group_name": "Garments", "interacted_at": "2026-08-08 15:45:00"}
        ]
    }
}

CUSTOMER_FEEDBACK_STORE = [
    {
        "feedback_id": "FB_2001",
        "customer_id": "CUST_10",
        "article_id": "0108775015",
        "rating": 5,
        "comment": "Perfect fit and high-quality material!",
        "created_at": "2026-08-08 16:20:00"
    }
]

# =====================================================================
# 🛠️ API ENDPOINTS
# =====================================================================

# --- 1. SEARCH & FILTER RECOMMENDATIONS ENDPOINT ---
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


# --- 2. PAGINATED HISTORY ENDPOINT ---
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


# --- 3. CUSTOMER SPECIFIC RECOMMENDATIONS ENDPOINT ---
@router.get(
    "/recommendations/{customer_id}",
    response_model=RecommendationResponse,
    summary="Get Customer Specific Recommendations"
)
def get_customer_recommendations(
    customer_id: str = Path(..., min_length=3, max_length=50, description="Customer ID"),
    limit: int = Query(10, ge=1, le=100, description="Limit returned items")
):
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


# --- 4. CUSTOMER PROFILE ENDPOINT ---
@router.get(
    "/customers/{customer_id}",
    response_model=CustomerProfileResponse,
    summary="Get Customer Profile Information",
    description="Retrieve contextual customer profile data including purchase history count and preferences."
)
def get_customer_profile(
    customer_id: str = Path(..., min_length=3, max_length=50, description="Customer ID (e.g., CUST_10)")
):
    try:
        clean_id = customer_id.strip().upper()
        
        if clean_id not in CUSTOMER_PROFILES_STORE:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with ID '{customer_id}' was not found in the records."
            )

        profile_data = CUSTOMER_PROFILES_STORE[clean_id]

        return CustomerProfileResponse(
            status="success",
            data=CustomerProfile(**profile_data)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving customer profile: {str(e)}"
        )


# --- 5. AGGREGATED CUSTOMER ACTIVITY ENDPOINT ---
@router.get(
    "/customers/{customer_id}/activity",
    response_model=AggregatedCustomerActivityResponse,
    summary="Get Aggregated Customer Activity Tree",
    description="Combines live recommendations, favorites, recently viewed items, recommendation history, and feedback."
)
def get_customer_activity_tree(
    customer_id: str = Path(..., min_length=3, max_length=50, description="Customer ID (e.g., CUST_10)")
):
    try:
        clean_id = customer_id.strip().upper()

        # 1. Live Recommendations
        live_recs = [RecommendationItem(**item) for item in CANDIDATE_UNIVERSE[:5]]

        # 2. Activity Store (Recently Viewed & Favorites)
        user_activity = CUSTOMER_ACTIVITY_STORE.get(clean_id, {"recently_viewed": [], "favorites": []})
        recently_viewed = [InteractionArticle(**item) for item in user_activity.get("recently_viewed", [])]
        favorites = [InteractionArticle(**item) for item in user_activity.get("favorites", [])]

        # 3. Recommendation History
        user_history = [
            HistoryRecord(**rec) for rec in RECOMMENDATION_HISTORY_STORE 
            if rec["customer_id"].upper() == clean_id
        ]

        # 4. Feedback
        user_feedback = [
            FeedbackItem(**fb) for fb in CUSTOMER_FEEDBACK_STORE 
            if fb["customer_id"].upper() == clean_id
        ]

        # 5. Activity Status Check
        has_activity = bool(recently_viewed or favorites or user_history or user_feedback)

        return AggregatedCustomerActivityResponse(
            status="success",
            customer_id=customer_id,
            has_activity=has_activity,
            data=CustomerActivityTreeData(
                customer_id=customer_id,
                recommendations=live_recs,
                favorites=favorites,
                recently_viewed=recently_viewed,
                recommendation_history=user_history,
                feedback=user_feedback
            )
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error aggregating customer activity: {str(e)}"
        )