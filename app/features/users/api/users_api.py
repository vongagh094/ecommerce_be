from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....shared.dependencies.database import get_db_session
from ....shared.dependencies.auth import verify_auth0_token, require_auth
from ..services.user_service import UserService
from ..schemas.auth0 import Auth0SyncRequest, Auth0SyncResponse
from loguru import logger

logger.add("logs/users_api.log", rotation="100 MB", retention="10 days")
router = APIRouter(prefix="/users", tags=["users"]) 


def get_user_service(db: Session = Depends(get_db_session)) -> UserService:
	return UserService(db)


@router.post("/auth0-sync", response_model=Auth0SyncResponse, status_code=200)
async def auth0_sync(
	payload: Auth0SyncRequest,
	_: dict = Depends(verify_auth0_token),
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
	
@router.get("/me", status_code=200)
async def get_me(user = Depends(require_auth)):
	"""Return current authenticated user."""
	return {
		"id": user.id,
		"auth0Id": user.auth0_id,
		"email": user.email,
		"name": user.full_name,
		"picture": user.profile_image_url,
	}

@router.put("/me", status_code=200)
async def update_profile(
	payload: dict,
	user = Depends(require_auth),
	service: UserService = Depends(get_user_service)
):
	"""Update current user's profile."""
	try:
		logger.info(f"Updating profile for user_id={user.id}")
		updated = await service.update_profile(
			user_id=user.id,
			name=payload.get("name"),
			picture=payload.get("picture"),
			phone_number=payload.get("phone_number"),
			gender=payload.get("gender")
		)
		return {
			"id": updated.id,
			"auth0Id": updated.auth0_id,
			"email": updated.email,
			"name": updated.full_name,
			"picture": updated.profile_image_url,
		}
	except HTTPException:
		raise
	except Exception:
		raise HTTPException(status_code=500, detail="Failed to update profile")

@router.get("/me/profile", status_code=200)
async def get_me_profile(user = Depends(require_auth)):
    return {
        "id": user.id,
        "auth0Id": user.auth0_id,
        "email": user.email,
        "name": user.full_name,
        "picture": user.profile_image_url,
        "phone_number": user.phone_number,
        "gender": user.gender,
        "host_about": user.host_about,
        "host_review_count": user.host_review_count,
        "host_rating_average": user.host_rating_average,
        "is_super_host": user.is_super_host,
    }

@router.get("/list/profiles", status_code=200)
async def get_list_profiles(
    offset: int = 0, 
    limit: int = 100, 
    service: UserService = Depends(get_user_service)
):
    return [
        {
            "id": user.id,
            "auth0Id": user.auth0_id,
            "email": user.email,
             "name": user.full_name,
             "picture": user.profile_image_url,
             "phone_number": user.phone_number,
             "gender": user.gender,
             "is_active": user.is_active,
             "host_about": user.host_about,
             "host_review_count": user.host_review_count,
             "host_rating_average": user.host_rating_average,
             "is_super_host": user.is_super_host,
         }
         for user in await service.get_all_users(offset=offset, limit=limit)
     ]

@router.put("/status/{user_id}", status_code=200)
async def update_user_status(
	user_id: int,
	status: str,
	service: UserService = Depends(get_user_service)
):
	"""Update user status."""
	try:
		user = await service.update_user_status(user_id=user_id, status=status)
		return {
			"is_active": user.is_active,
		}
	except HTTPException:
		raise
	except Exception:
		raise HTTPException(status_code=500, detail="Failed to update user status")