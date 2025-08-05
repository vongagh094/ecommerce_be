from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, case, or_, func
from sqlalchemy.orm import joinedload
from app.features.messages.schemas.ConversationDTO import ConversationCreateDTO, ConversationResponseDTO
from app.db.models.conversation import Conversation
from app.db.models.user import User
from app.db.models.property import Property
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, data: ConversationCreateDTO) -> ConversationResponseDTO:
        """Create a new conversation."""
        try:
            conversation = Conversation(**data.model_dump())
            conversation.is_archived = False
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
            return ConversationResponseDTO.model_validate(conversation)
        except Exception as e:
            self.db.rollback()
            logger.error(f"Lỗi khi tạo cuộc trò chuyện: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")

    def get_conversations_by_user(self, user_id: int) -> List[ConversationResponseDTO]:
        """Get all conversations by user ID with property title and other user info."""
        try:
            query = (
                select(
                    Conversation,
                    Property.title.label("property_title"),
                    case(
                        (Conversation.guest_id == user_id, User.full_name),
                        else_=User.full_name
                    ).label("other_user_full_name"),
                    case(
                        (Conversation.guest_id == user_id, User.id),
                        else_=User.id
                    ).label("other_user_id"),
                    case(
                        (Conversation.guest_id == user_id, User.username),
                        else_=User.username
                    ).label("other_user_username"),
                    case(
                        (Conversation.guest_id == user_id, User.email),
                        else_=User.email
                    ).label("other_user_email")
                )
                .outerjoin(Property, Conversation.property_id == Property.id)
                .join(User, or_(Conversation.guest_id == User.id, Conversation.host_id == User.id))
                .where(or_(Conversation.guest_id == user_id, Conversation.host_id == user_id))
                .where(User.id != user_id)
                .order_by(Conversation.last_message_at.desc().nulls_last())
                .options(joinedload(Conversation.property))
            )
            logger.debug(f"Thực thi truy vấn: {str(query)}")
            result = self.db.execute(query).unique()
            conversations = result.all()

            if not conversations:
                logger.info(f"Không tìm thấy cuộc trò chuyện cho user_id {user_id}")
                return []

            return [
                ConversationResponseDTO(
                    id=conv.Conversation.id,
                    property_id=conv.Conversation.property_id,
                    guest_id=conv.Conversation.guest_id,
                    host_id=conv.Conversation.host_id,
                    last_message_at=conv.Conversation.last_message_at,
                    is_archived=conv.Conversation.is_archived,
                    created_at=conv.Conversation.created_at,
                    name=conv.other_user_full_name,
                    property_title=conv.property_title,
                    other_user={
                        "id": conv.other_user_id,
                        "username": conv.other_user_username or "",
                        "full_name": conv.other_user_full_name or "",
                        "email": conv.other_user_email
                    }
                ) for conv in conversations
            ]
        except Exception as e:
            logger.error(f"Lỗi khi lấy danh sách cuộc trò chuyện: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")

    def get_conversations_by_property(self, property_id: int) -> List[ConversationResponseDTO]:
        """Get all conversations by property ID with property title and other user info."""
        try:
            query = (
                select(
                    Conversation,
                    Property.title.label("property_title"),
                    case(
                        (Conversation.guest_id == Conversation.host_id, User.full_name),
                        else_=User.full_name
                    ).label("other_user_full_name"),
                    case(
                        (Conversation.guest_id == Conversation.host_id, User.id),
                        else_=User.id
                    ).label("other_user_id"),
                    case(
                        (Conversation.guest_id == Conversation.host_id, User.username),
                        else_=User.username
                    ).label("other_user_username"),
                    case(
                        (Conversation.guest_id == Conversation.host_id, User.email),
                        else_=User.email
                    ).label("other_user_email")
                )
                .outerjoin(Property, Conversation.property_id == Property.id)
                .join(User, or_(Conversation.guest_id == User.id, Conversation.host_id == User.id))
                .where(Conversation.property_id == property_id)
                .order_by(Conversation.last_message_at.desc().nulls_last())
                .options(joinedload(Conversation.property))
            )
            logger.debug(f"Thực thi truy vấn: {str(query)}")
            result = self.db.execute(query).unique()
            conversations = result.all()

            if not conversations:
                logger.info(f"Không tìm thấy cuộc trò chuyện cho property_id {property_id}")
                return []

            return [
                ConversationResponseDTO(
                    id=conv.Conversation.id,
                    property_id=conv.Conversation.property_id,
                    guest_id=conv.Conversation.guest_id,
                    host_id=conv.Conversation.host_id,
                    last_message_at=conv.Conversation.last_message_at,
                    is_archived=conv.Conversation.is_archived,
                    created_at=conv.Conversation.created_at,
                    name=conv.other_user_full_name,
                    property_title=conv.property_title,
                    other_user={
                        "id": conv.other_user_id,
                        "username": conv.other_user_username or "",
                        "full_name": conv.other_user_full_name or "",
                        "email": conv.other_user_email
                    }
                ) for conv in conversations
            ]
        except Exception as e:
            logger.error(f"Lỗi khi lấy danh sách cuộc trò chuyện theo property_id: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")

    def validate_user(self, user_id: int) -> bool:
        """Validate if user exists."""
        user_exists = self.db.scalar(select(User.id).where(User.id == user_id))
        return bool(user_exists)

    def validate_property(self, property_id: int) -> bool:
        """Validate if property exists."""
        property_exists = self.db.scalar(select(Property.id).where(Property.id == property_id))
        return bool(property_exists)

    def validate_users_and_property(self, host_id: int, guest_id: int, property_id: Optional[int]) -> bool:
        """Validate if host_id, guest_id, and property_id (if provided) exist."""
        users = self.db.execute(select(User.id).where(User.id.in_([host_id, guest_id])))
        user_ids = users.scalars().all()
        if len(user_ids) != 2:
            return False

        if property_id:
            property_exists = self.db.scalar(select(Property.id).where(Property.id == property_id))
            return bool(property_exists)
        return True

    def get_existing_conversation(self, host_id: int, guest_id: int, property_id: Optional[int]) -> Optional[ConversationResponseDTO]:
        """Check if a conversation with the given host_id, guest_id, and property_id exists."""
        query = (
            select(Conversation)
            .where(Conversation.host_id == host_id)
            .where(Conversation.guest_id == guest_id)
            .where(Conversation.property_id == property_id)
        )
        conversation = self.db.execute(query).scalar_one_or_none()
        if conversation:
            return ConversationResponseDTO.model_validate(conversation)
        return None

    def validate_user_in_conversation(self, user_id: int, conversation_id: int) -> bool:
        """Validate if user belongs to the conversation."""
        conv_exists = self.db.scalar(
            select(Conversation.id)
            .where(Conversation.id == conversation_id)
            .where(or_(Conversation.guest_id == user_id, Conversation.host_id == user_id))
        )
        return bool(conv_exists)

    def update_last_message_at(self, conversation_id: int) -> None:
        """Update the last_message_at timestamp for a conversation."""
        try:
            self.db.execute(
                Conversation.__table__.update()
                .where(Conversation.id == conversation_id)
                .values(last_message_at=func.current_timestamp())
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(f"Lỗi khi cập nhật last_message_at: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")