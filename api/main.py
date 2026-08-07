from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api.routes import router

app = FastAPI(
    title="Context-Aware Neural Recommendation Engine API",
    version="1.2.0"
)

# Custom Exception Handler for Validation Errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "error_code": "VALIDATION_ERROR",
            "message": "Input validation failed. Please check query parameter constraints.",
            "details": exc.errors()
        }
    )

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Recommendation Engine API Operational"}