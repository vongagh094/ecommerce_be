"""CORS middleware setup."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ...core.config import settings


def setup_cors(app: FastAPI) -> None:
    """Setup CORS middleware."""
    # allow all cors
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # <- Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # <- Allow all methods
        allow_headers=["*"],  # <- Allow all headers
    )