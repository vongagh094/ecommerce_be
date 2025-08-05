"""Authentication dependencies."""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
import jwt

from ..models import User
from ..exceptions import AuthenticationError, TokenExpiredError, InvalidTokenError
from .database import get_db_session
from ...core.config import settings

security = HTTPBearer(auto_error=False)


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db_session)
) -> Optional[User]:
    """Get current user if authenticated, None otherwise."""
    
    if not credentials:
        return None
    
    try:
        return await _decode_token_and_get_user(credentials.credentials, db)
    except (AuthenticationError, TokenExpiredError, InvalidTokenError):
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
) -> User:
    """Get current authenticated user."""
    
    if not credentials:
        raise AuthenticationError("No token provided")
    
    return await _decode_token_and_get_user(credentials.credentials, db)


def require_auth(user: User = Depends(get_current_user)) -> User:
    """Require authentication dependency."""
    return user


async def _decode_token_and_get_user(token: str, db: Session) -> User:
    """Decode JWT token and get user."""
    
    try:
        # Decode JWT token
        payload = jwt.decode(
            token, 
            settings.auth0.public_key, 
            algorithms=["RS256"],
            audience=settings.auth0.audience
        )
        
        # Get user from database
        auth0_id = payload.get("sub")
        if not auth0_id:
            raise InvalidTokenError("Invalid token payload")
        
        user = db.query(User).filter(User.auth0_id == auth0_id).first()
        if not user:
            raise AuthenticationError("User not found")
        
        if not user.is_active:
            raise AuthenticationError("User account is disabled")
        
        return user
        
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except jwt.InvalidTokenError:
        raise InvalidTokenError()
    except Exception as e:
        raise AuthenticationError(f"Authentication failed: {str(e)}")