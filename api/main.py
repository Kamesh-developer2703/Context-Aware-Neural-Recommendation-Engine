from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Context-Aware Neural Recommendation Engine",
    description="Recommendation API for personalized article recommendations",
    version="1.1.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "Recommendation Engine API Running Successfully"
    }

@app.get("/health")
def health():
    return {
        "status": "Healthy",
        "api": "Recommendation Engine",
        "version": "1.1.0"
    }