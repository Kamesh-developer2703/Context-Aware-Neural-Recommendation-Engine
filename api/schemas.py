from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    article_id: int
    score: float


class FavoriteArticle(BaseModel):
    article_id: int


class FavoriteResponse(BaseModel):
    status: str
    article_id: int