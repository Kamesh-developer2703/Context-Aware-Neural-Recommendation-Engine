from pydantic import BaseModel, Field


class RecommendationResponse(BaseModel):
    article_id: int
    score: float


class FavoriteArticle(BaseModel):
    article_id: int = Field(
        ...,
        gt=0,
        description="Positive article ID"
    )


class FavoriteResponse(BaseModel):
    status: str
    article_id: int