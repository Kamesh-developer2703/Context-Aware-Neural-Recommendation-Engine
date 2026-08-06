from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException, status
from api.schemas import RecommendationResponse, RecommendationItem

router = APIRouter()

# Mock Candidate Universe (Simulates neural candidate retrieval output)
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

@router.get(
    "/recommendations/search",
    response_model=RecommendationResponse,
    summary="Search and Filter Recommendations",
    description="Search recommendations by keyword/product type, filter by minimum similarity score, customer ID, and set Top-K limits."
)
def search_and_filter_recommendations(
    customer_id: Optional[str] = Query(None, description="Customer ID for contextual personalization"),
    query: Optional[str] = Query(None, description="Search term for article ID or product type (e.g., 'Dress', 'Shoes')"),
    min_score: float = Query(0.0, ge=0.0, le=1.0, description="Filter out items below this similarity score"),
    top_k: int = Query(10, ge=1, le=100, description="Top-K limit on number of returned items")
):
    try:
        # Step 1: Base Candidate Collection
        results = CANDIDATE_UNIVERSE.copy()

        # Step 2: Apply Search Query Filter (Article ID or Product Type match)
        if query:
            q_clean = query.strip().lower()
            results = [
                item for item in results 
                if q_clean in item["product_type"].lower() or q_clean in item["article_id"].lower()
            ]

        # Step 3: Apply Minimum Score Threshold Filter
        results = [item for item in results if item["score"] >= min_score]

        # Step 4: Ensure Strict Descending Rank Logic
        results.sort(key=lambda x: x["score"], reverse=True)

        # Step 5: Enforce Top-K Limit
        total_found = len(results)
        final_recs = results[:top_k]

        # Step 6: Validate output
        if total_found == 0:
            return RecommendationResponse(
                status="success",
                customer_id=customer_id,
                search_query=query,
                min_score_filter=min_score,
                total_found=0,
                returned_count=0,
                recommendations=[]
            )

        return RecommendationResponse(
            status="success",
            customer_id=customer_id,
            search_query=query,
            min_score_filter=min_score,
            total_found=total_found,
            returned_count=len(final_recs),
            recommendations=[RecommendationItem(**item) for item in final_recs]
        )

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid parameter value: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing recommendations: {str(e)}"
        )