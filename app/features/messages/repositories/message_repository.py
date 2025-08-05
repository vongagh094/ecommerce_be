from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, update
from app.features.messages.schemas.MessageDTO import MessageCreateDTO, MessageResponseDTO, MessageUpdateDTO
from app.db.models.message import Message
from app.db.models.user import User
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, data: MessageCreateDTO) -> MessageResponseDTO:
        """Create a new message."""
        try:
            # Exclude mark_as_read from the data passed to the Message model
            message_data = data.model_dump(exclude={'mark_as_read'})
            message = Message(**message_data)
            self.db.add(message)
            self.db.commit()
            self.db.refresh(message)
            
            # Fetch sender details
            sender = self.db.execute(select(User).where(User.id == message.sender_id)).scalar_one_or_none()
            if not sender:
                logger.error(f"Không tìm thấy người gửi với ID {message.sender_id}")
                raise HTTPException(status_code=404, detail="Không tìm thấy người gửi")
            
            return MessageResponseDTO(
                id=message.id,
                conversation_id=message.conversation_id,
                sender_id=message.sender_id,
                message_text=message.message_text,
                is_read=message.is_read,
                sent_at=message.sent_at,
                sender={
                    "id": sender.id,
                    "username": sender.username or "",
                    "full_name": sender.full_name or "",
                    "email": sender.email
                }
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"Lỗi khi tạo tin nhắn: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")

    def get_messages(self, conversation_id: int, limit: int, offset: int) -> List[MessageResponseDTO]:
        """Get messages by conversation ID."""
        try:
            query = (
                select(Message, User)
                .join(User, Message.sender_id == User.id)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.sent_at.desc())
                .offset(offset)
                .limit(limit)
            )
            messages = self.db.execute(query).all()

            return [
                MessageResponseDTO(
                    id=msg.Message.id,
                    conversation_id=msg.Message.conversation_id,
                    sender_id=msg.Message.sender_id,
                    message_text=msg.Message.message_text,
                    is_read=msg.Message.is_read,
                    sent_at=msg.Message.sent_at,
                    sender={
                        "id": msg.User.id,
                        "username": msg.User.username or "",
                        "full_name": msg.User.full_name or "",
                        "email": msg.User.email
                    }
                ) for msg in messages
            ]
        except Exception as e:
            logger.error(f"Lỗi khi lấy tin nhắn: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")

    def update_message(self, message_id: int, data: MessageUpdateDTO) -> Optional[MessageResponseDTO]:
        """Update a message's read status."""
        try:
            message = self.db.execute(
                select(Message).where(Message.id == message_id)
            ).scalar_one_or_none()
            if not message:
                return None
            
            if data.is_read is not None:
                message.is_read = data.is_read
            
            self.db.commit()
            self.db.refresh(message)

            sender = self.db.execute(select(User).where(User.id == message.sender_id)).scalar_one_or_none()
            if not sender:
                logger.error(f"Không tìm thấy người gửi với ID {message.sender_id}")
                raise HTTPException(status_code=404, detail="Không tìm thấy người gửi")

            return MessageResponseDTO(
                id=message.id,
                conversation_id=message.conversation_id,
                sender_id=message.sender_id,
                message_text=message.message_text,
                is_read=message.is_read,
                sent_at=message.sent_at,
                sender={
                    "id": sender.id,
                    "username": sender.username or "",
                    "full_name": sender.full_name or "",
                    "email": sender.email
                }
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"Lỗi khi cập nhật tin nhắn: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")

    def validate_sender_and_conversation(self, sender_id: int, conversation_id: int) -> bool:
        """Validate if sender belongs to the conversation."""
        from app.db.models.conversation import Conversation
        conversation = self.db.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(or_(Conversation.guest_id == sender_id, Conversation.host_id == sender_id))
        ).scalar_one_or_none()
        return bool(conversation)

    def mark_messages_as_read(self, conversation_id: int, user_id: int) -> List[MessageResponseDTO]:
        """Mark all unread messages in a conversation as read for a user."""
        try:
            messages = self.db.execute(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .where(Message.sender_id != user_id)
                .where(Message.is_read == False)
            ).scalars().all()

            if not messages:
                return []

            for message in messages:
                message.is_read = True

            self.db.commit()

            updated_messages = []
            for message in messages:
                sender = self.db.execute(select(User).where(User.id == message.sender_id)).scalar_one_or_none()
                if not sender:
                    logger.error(f"Không tìm thấy người gửi với ID {message.sender_id}")
                    continue
                updated_messages.append(
                    MessageResponseDTO(
                        id=message.id,
                        conversation_id=message.conversation_id,
                        sender_id=message.sender_id,
                        message_text=message.message_text,
                        is_read=message.is_read,
                        sent_at=message.sent_at,
                        sender={
                            "id": sender.id,
                            "username": sender.username or "",
                            "full_name": sender.full_name or "",
                            "email": sender.email
                        }
                    )
                )
            return updated_messages
        except Exception as e:
            self.db.rollback()
            logger.error(f"Lỗi khi đánh dấu tin nhắn đã đọc: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")