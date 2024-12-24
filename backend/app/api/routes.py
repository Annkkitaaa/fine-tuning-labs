from fastapi import APIRouter
from .endpoints import model_endpoints, training_endpoints

router = APIRouter()
router.include_router(model_endpoints.router)
router.include_router(training_endpoints.router)