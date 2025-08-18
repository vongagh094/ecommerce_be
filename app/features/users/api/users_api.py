from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....shared.dependencies.database import get_db_session
from ....shared.dependencies.auth import require_auth
from ..services.user_service import UserService
from ..schemas.auth0 import Auth0SyncRequest, Auth0SyncResponse

router = APIRouter(prefix="/users", tags=["users"]) 


def get_user_service(db: Session = Depends(get_db_session)) -> UserService:
	return UserService(db)


@router.post("/auth0-sync", response_model=Auth0SyncResponse, status_code=200)
async def auth0_sync(
	payload: Auth0SyncRequest,
	_: dict = Depends(require_auth),
	service: UserService = Depends(get_user_service)
):
	"""Upsert user by Auth0 user id and return canonical user payload."""
	try:
		user = await service.upsert_by_auth0(
			auth0_id=payload.auth0UserId,
			email=payload.email,
			email_verified=payload.emailVerified,
			name=payload.name,
			picture=payload.picture,
		)
		return Auth0SyncResponse(
			id=user.id,
			auth0UserId=user.auth0_id,
			email=user.email,
			name=user.full_name if user.full_name else None,
			picture=user.profile_image_url if user.profile_image_url else None,
			createdAt=user.created_at,
		)
	except UserService.EmailConflictError as e:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
	except HTTPException:
		raise
	except Exception:
		raise HTTPException(status_code=500, detail="Failed to sync user") 