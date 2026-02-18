from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import json
import logging

from app.db.sql.base_class import Base
from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from app.api.routers import api  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json", debug=True
)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api.api_router, prefix=settings.API_V1_STR)

assert settings.SQLALCHEMY_DATABASE_URI is not None, "SQLALCHEMY_DATABASE_URI must be set"
engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    pool_size=300,
    max_overflow=600,
    pool_timeout=60,
    pool_recycle=1800
)