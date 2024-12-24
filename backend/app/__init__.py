from fastapi import FastAPI
from .api.routes import router as api_router

app = FastAPI(title="Fine-Tuning Labs")
app.include_router(api_router, prefix="/api")