from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core.database import engine
from app.db.base import Base
from app.api.v1.router import api_router as api_v1_router
from app.users.exceptions import (
    PermissionDenied, NotFound,
    )

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Task Manager API",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(api_v1_router, prefix="/api")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


@app.exception_handler(PermissionDenied)
async def permission_denied_handler(
    request: Request,
    exc: PermissionDenied,
):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc) or "Permission denied"},
    )


@app.exception_handler(NotFound)
async def not_found_handler(
    request: Request,
    exc: NotFound,
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc) or "Resource not found"},
    )


"""
generate a full conftest.py

show async Postgres test isolation

create reusable user/admin factories

add property-based tests for phone normalization
"""