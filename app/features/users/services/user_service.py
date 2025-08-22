from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.models.user import User

class UserService:
	class EmailConflictError(Exception):
		pass

	def __init__(self, db: Session):
		self.db = db

	async def upsert_by_auth0(
		self,
		auth0_id: str,
		email: str,
		email_verified: bool,
		name: Optional[str] = None,
		picture: Optional[str] = None,
	) -> User:
		"""Upsert a user by Auth0 ID. If exists, update; otherwise create."""
		# If email is verified, ensure no conflict with an existing different user
		if email_verified:
			existing_by_email = self.db.query(User).filter(User.email == email).first()
			if existing_by_email and existing_by_email.auth0_id and existing_by_email.auth0_id != auth0_id:
				raise self.EmailConflictError("Email is already linked to another account")

		user = self.db.query(User).filter(User.auth0_id == auth0_id).first()
		if user:
			# Update
			user.email = email or user.email
			if name:
				user.full_name = name
			if picture:
				user.profile_image_url = picture
			# Mark verified
			user.verification_status = "VERIFIED" if email_verified else user.verification_status
		else:
			# Create
			user = User(
				auth0_id=auth0_id,
				email=email,
				username=email,  # default username from email
				full_name=name or email.split("@")[0],
				profile_image_url=picture,
				verification_status="VERIFIED" if email_verified else None,
				is_active=True,
			)
			self.db.add(user)

		self.db.commit()
		self.db.refresh(user)
		return user

	async def update_profile(
		self,
		user_id: int,
		name: Optional[str] = None,
		picture: Optional[str] = None,
		phone_number: Optional[str] = None,
		gender: Optional[str] = None,
	) -> User:
		"""Update allowed profile fields for a user."""
		user = self.db.query(User).filter(User.id == user_id).first()
		if not user:
			raise ValueError("User not found")

		if name is not None:
			user.full_name = name
		if picture is not None:
			user.profile_image_url = picture
		if phone_number is not None:
			user.phone_number = phone_number
		if gender is not None:
			user.gender = gender

		self.db.commit()
		self.db.refresh(user)
		return user 

	async def get_all_users(self, offset: int = 0, limit: int = 100) -> list[User]:
		"""Get a list of all users."""
		return self.db.query(User).order_by(User.created_at).offset(offset).limit(limit).all()

	async def update_user_status(self, user_id: int, status: str) -> User:
		"""Update the status of a user."""
		user = self.db.query(User).filter(User.id == user_id).first()
		if not user:
			raise ValueError("User not found")

		if status == 'false':
			user.is_active = False
		else:
			user.is_active = True

		self.db.commit()
		self.db.refresh(user)
		return user