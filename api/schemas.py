from pydantic import BaseModel

class RecommendationResponse(BaseModel):
    article_id: int
    score: float