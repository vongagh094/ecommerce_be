"""Pagination dependencies."""

from fastapi import Query
from ..schemas.pagination import PaginationParams
from ..constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(
        DEFAULT_PAGE_SIZE, 
        ge=1, 
        le=MAX_PAGE_SIZE, 
        description="Items per page"
    )
) -> PaginationParams:
    """Get pagination parameters."""
    return PaginationParams(page=page, limit=limit)