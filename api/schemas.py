from typing import List, Optional
from pydantic import BaseModel, Field

# =====================================================================
# 📦 RECOMMENDATION SCHEMAS
# =====================================================================

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

# =====================================================================
# 📜 HISTORY SCHEMAS
# =====================================================================

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

# =====================================================================
# 👤 CUSTOMER PROFILE SCHEMAS
# =====================================================================

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

# =====================================================================
# 🌳 AGGREGATED CUSTOMER ACTIVITY & FEEDBACK SCHEMAS
# =====================================================================

class InteractionArticle(BaseModel):
    article_id: str
    product_type: str
    product_group_name: Optional[str] = "Garments"
    interacted_at: str

class FeedbackItem(BaseModel):
    feedback_id: str
    article_id: str
    rating: int = Field(..., ge=1, le=5, description="Rating between 1 and 5 stars")
    comment: Optional[str] = None
    created_at: str

class CustomerActivityTreeData(BaseModel):
    customer_id: str
    recommendations: List[RecommendationItem] = []
    favorites: List[InteractionArticle] = []
    recently_viewed: List[InteractionArticle] = []
    recommendation_history: List[HistoryRecord] = []
    feedback: List[FeedbackItem] = []

class AggregatedCustomerActivityResponse(BaseModel):
    status: str
    customer_id: str
    has_activity: bool
    data: CustomerActivityTreeData

# =====================================================================
# ⚠️ ERROR SCHEMAS
# =====================================================================

class ErrorResponse(BaseModel):
    status: str
    error_code: str
    message: str
    details: Optional[dict] = None


# --- TRENDING ARTICLES SCHEMAS ---
class TrendingArticle(BaseModel):
    article_id: str
    product_type: str
    product_group_name: Optional[str] = "Garments"
    popularity_score: float
    total_interactions: int

class TrendingResponse(BaseModel):
    status: str
    limit: int
    total_trending: int
    data: List[TrendingArticle]

class SimilarArticleItem(BaseModel):
    article_id: str
    similarity_score: float = Field(..., ge=0.0, le=1.0, description="Cosine similarity score")
    product_type: str
    product_group_name: Optional[str] = "Garments"

class SimilarArticlesResponse(BaseModel):
    status: str
    target_article_id: str
    limit: int
    total_found: int
    data: List[SimilarArticleItem]