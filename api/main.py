from fastapi import FastAPI

from api.routes import router

app = FastAPI(

    title="Context-Aware Neural Recommendation Engine",

    description="""
Recommendation Engine API

Features

• Personalized Recommendations

• Top-K Recommendation

• Health Monitoring

• Swagger Documentation

""",

    version="1.2"
)

app.include_router(router)


@app.get("/")
def home():

    return{

        "message":"Recommendation API Running",

        "version":"1.2"
    }


@app.get("/health")
def health():

    return{

        "status":"Healthy",

        "model":"Two Tower ANN",

        "version":"1.2"
    }