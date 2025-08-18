from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class Auth0SyncRequest(BaseModel):
	auth0UserId: str
	email: EmailStr
	emailVerified: bool
	name: Optional[str] = None
	picture: Optional[str] = None


class Auth0SyncResponse(BaseModel):
	id: int
	auth0UserId: str
	email: EmailStr
	name: Optional[str] = None
	picture: Optional[str] = None
	createdAt: datetime 