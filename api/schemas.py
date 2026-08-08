from typing import List, Optional
from pydantic import BaseModel, Field

# Individual Item Model
class RecommendationItem(BaseModel):
    article_id: str
    score: float
    product_type: str
    product_group_name: Optional[str] = "Garments"

# Single & Search Recommendation Response Model
class RecommendationResponse(BaseModel):
    status: str
    customer_id: Optional[str] = None
    search_query: Optional[str] = None
    min_score_filter: Optional[float] = None
    total_found: int
    returned_count: int
    recommendations: List[RecommendationItem]

# History Record Item Model
class HistoryRecord(BaseModel):
    recommendation_id: str
    customer_id: str
    timestamp: str
    items_recommended: List[RecommendationItem]

# Paginated History Response Model
class PaginatedHistoryResponse(BaseModel):
    status: str
    customer_id: Optional[str] = None
    page: int
    limit: int
    total_records: int
    total_pages: int
    has_next: bool
    has_prev: bool
    history: List[HistoryRecord]

# Standard Error Response Model
class ErrorResponse(BaseModel):
    status: str
    error_code: str
    message: str
    details: Optional[dict] = None