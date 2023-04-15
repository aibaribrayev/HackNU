from fastapi import FastAPI

from core.config import settings
from db.repositories.some_repository import SomeRepository
from core.services.some_service import SomeService

app = FastAPI()

# Initialize database repository and service
some_repository = SomeRepository()
some_service = SomeService(some_repository)

# Include API endpoints
from api.v1.endpoints.some_endpoint import router as some_router
app.include_router(some_router, prefix="/some")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level=settings.LOG_LEVEL,
        reload=settings.DEBUG_MODE,
    )
