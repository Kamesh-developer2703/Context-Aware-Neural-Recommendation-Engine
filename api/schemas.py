from typing import List, Optional
from pydantic import BaseModel, Field

# --- EXISTING SCHEMAS ---
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

class HistoryRecord(BaseModel):
    recommendation_id: str
    customer_id: str
    timestamp: str
    items_recommended: List[RecommendationItem]

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

# --- NEW CUSTOMER PROFILE SCHEMAS ---
class CustomerPreferences(BaseModel):
    preferred_categories: List[str]
    frequent_sizes: List[str]
    favorite_colors: List[str]

class CustomerProfile(BaseModel):
    customer_id: str = Field(..., min_length=3, max_length=50, description="Unique customer identifier")
    name: str
    email: str
    membership_status: str
    age_group: Optional[str] = "25-34"
    total_purchases: int
    preferences: CustomerPreferences

class CustomerProfileResponse(BaseModel):
    status: str
    data: CustomerProfile

class ErrorResponse(BaseModel):
    status: str
    error_code: str
    message: str
    details: Optional[dict] = None