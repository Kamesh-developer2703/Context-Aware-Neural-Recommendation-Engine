from typing import List, Optional
from pydantic import BaseModel, Field

class RecommendationItem(BaseModel):
    article_id: str
    score: float
    product_type: str
    product_group_name: Optional[str] = "Garments"

class RecommendationResponse(BaseModel):
    status: str
    customer_id: Optional[str] = None
    search_query: Optional[str] = None
    min_score_filter: Optional[float] = None
    total_found: int
    returned_count: int
    recommendations: List[RecommendationItem]

class ErrorResponse(BaseModel):
    status: str
    error_code: str
    message: str