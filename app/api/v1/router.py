from fastapi import APIRouter
from .users import router as users_router
# from .tasks import router as tasks_router
# from .assignments import router as assignments_router

api_router = APIRouter(prefix="/v1")

api_router.include_router(users_router, prefix="/users", tags=["users"])
# api_router.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
# api_router.include_router(assignments_router, prefix="/assignments", tags=["assignments"])
