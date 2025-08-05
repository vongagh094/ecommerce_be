from typing import Optional, List
from fastapi import HTTPException
import logging
from app.features.messages.schemas.MessageDTO import MessageCreateDTO, MessageResponseDTO, MessageUpdateDTO
from app.features.messages.schemas.ConversationDTO import ConversationCreateDTO, ConversationResponseDTO
from app.features.messages.repositories.message_repository import MessageRepository
from app.features.messages.repositories.conversation_repository import ConversationRepository
from app.features.messages.services.pusher_service import PusherService

logger = logging.getLogger(__name__)

class MessageService:
    def __init__(self, message_repository: MessageRepository, conversation_repository: ConversationRepository, pusher_service: PusherService):
        self.message_repository = message_repository
        self.conversation_repository = conversation_repository
        self.pusher_service = pusher_service

    def create_message(self, data: MessageCreateDTO) -> MessageResponseDTO:
        logger.info(f"Nhận yêu cầu tạo tin nhắn: {data.model_dump()}")
        try:
            if not data.message_text:
                logger.warning("Yêu cầu message_text để gửi tin nhắn")
                raise HTTPException(status_code=400, detail="Yêu cầu message_text để gửi tin nhắn")

            # Kiểm tra user_id và conversation_id
            if not self.message_repository.validate_sender_and_conversation(data.sender_id, data.conversation_id):
                logger.warning(f"sender_id {data.sender_id} không thuộc conversation_id {data.conversation_id}")
                raise HTTPException(status_code=403, detail="Người dùng không thuộc cuộc trò chuyện")

            # Tạo tin nhắn
            message = self.message_repository.create_message(data)

            # Cập nhật last_message_at
            self.conversation_repository.update_last_message_at(data.conversation_id)

            # Gửi sự kiện new-message qua Pusher
            try:
                logger.info(f"Gửi sự kiện new-message cho conversation-{data.conversation_id}")
                self.pusher_service.trigger_new_message(data.conversation_id, message)
            except Exception as e:
                logger.error(f"Lỗi gửi sự kiện Pusher: {str(e)}")

            return message
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Lỗi không mong muốn: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")

    def create_or_update_message(self, data: MessageCreateDTO) -> MessageResponseDTO | dict:
        logger.info(f"Nhận yêu cầu tạo/cập nhật tin nhắn: {data.model_dump()}")
        try:
            if data.mark_as_read and data.conversation_id and data.sender_id:
                if not self.conversation_repository.validate_user_in_conversation(data.sender_id, data.conversation_id):
                    logger.warning(f"sender_id {data.sender_id} không thuộc conversation_id {data.conversation_id}")
                    raise HTTPException(status_code=403, detail="Người dùng không thuộc cuộc trò chuyện")
                updated_messages = self.message_repository.mark_messages_as_read(data.conversation_id, data.sender_id)
                if updated_messages:
                    try:
                        logger.info(f"Gửi sự kiện messages-read cho conversation-{data.conversation_id}")
                        self.pusher_service.trigger_messages_read(data.conversation_id, updated_messages)
                    except Exception as e:
                        logger.error(f"Lỗi gửi sự kiện Pusher: {str(e)}")
                return {"success": True, "updatedMessages": updated_messages}
            return self.create_message(data)
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Lỗi không mong muốn: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")

    def get_messages(self, conversation_id: int, user_id: int, limit: int, offset: int) -> List[MessageResponseDTO]:
        logger.info(f"Nhận yêu cầu lấy tin nhắn: conversation_id={conversation_id}, user_id={user_id}, limit={limit}, offset={offset}")
        try:
            # Kiểm tra user_id và conversation_id
            if not self.conversation_repository.validate_user_in_conversation(user_id, conversation_id):
                logger.info(f"Không tìm thấy user_id {user_id} trong conversation_id {conversation_id}")
                return []

            # Lấy tin nhắn
            messages = self.message_repository.get_messages(conversation_id, limit, offset)

            # Cập nhật trạng thái đọc và gửi sự kiện Pusher
            updated_messages = self.message_repository.mark_messages_as_read(conversation_id, user_id)
            if updated_messages:
                try:
                    logger.info(f"Gửi sự kiện messages-read qua Pusher cho conversation-{conversation_id}")
                    self.pusher_service.trigger_messages_read(conversation_id, updated_messages)
                except Exception as e:
                    logger.error(f"Lỗi gửi sự kiện Pusher: {str(e)}")

            # Đảo ngược danh sách để trả về theo thứ tự thời gian
            return messages[::-1]
        except Exception as e:
            logger.error(f"Lỗi không mong muốn: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")

    def create_conversation(self, data: ConversationCreateDTO) -> ConversationResponseDTO:
        logger.info(f"Tạo cuộc trò chuyện: host_id={data.host_id}, guest_id={data.guest_id}, property_id={data.property_id}")
        try:
            # Kiểm tra host_id, guest_id, và property_id
            if not self.conversation_repository.validate_users_and_property(data.host_id, data.guest_id, data.property_id):
                logger.warning(f"host_id {data.host_id}, guest_id {data.guest_id}, hoặc property_id {data.property_id} không hợp lệ")
                raise HTTPException(status_code=400, detail="host_id, guest_id hoặc property_id không hợp lệ")

            # Kiểm tra cuộc trò chuyện đã tồn tại
            existing_conv = self.conversation_repository.get_existing_conversation(data.host_id, data.guest_id, data.property_id)
            if existing_conv:
                logger.info(f"Cuộc trò chuyện đã tồn tại với id: {existing_conv.id}")
                return existing_conv

            # Tạo cuộc trò chuyện mới
            return self.conversation_repository.create_conversation(data)
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Lỗi không mong muốn: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")

    def get_conversations_by_user(self, user_id: int) -> List[ConversationResponseDTO]:
        logger.info(f"Nhận yêu cầu lấy danh sách cuộc trò chuyện cho user_id: {user_id}")
        try:
            # Kiểm tra user_id
            if not self.conversation_repository.validate_user(user_id):
                logger.info(f"Không tìm thấy người dùng {user_id}, trả về danh sách rỗng")
                return []

            # Lấy danh sách cuộc trò chuyện
            conversations = self.conversation_repository.get_conversations_by_user(user_id)
            return conversations
        except Exception as e:
            logger.error(f"Lỗi không mong muốn: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")

    def get_conversations_by_property(self, property_id: int) -> List[ConversationResponseDTO]:
        logger.info(f"Nhận yêu cầu lấy danh sách cuộc trò chuyện cho property_id: {property_id}")
        try:
            # Kiểm tra property_id
            if not self.conversation_repository.validate_property(property_id):
                logger.info(f"Không tìm thấy property_id {property_id}, trả về danh sách rỗng")
                return []

            # Lấy danh sách cuộc trò chuyện
            conversations = self.conversation_repository.get_conversations_by_property(property_id)
            return conversations
        except Exception as e:
            logger.error(f"Lỗi không mong muốn: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")

    def update_message(self, message_id: int, data: MessageUpdateDTO) -> Optional[MessageResponseDTO]:
        logger.info(f"Nhận yêu cầu cập nhật tin nhắn: message_id={message_id}, data={data.model_dump()}")
        try:
            message = self.message_repository.update_message(message_id, data)
            if message:
                # Gửi sự kiện messages-read qua Pusher
                try:
                    logger.info(f"Gửi sự kiện messages-read qua Pusher cho conversation-{message.conversation_id}")
                    self.pusher_service.trigger_messages_read(message.conversation_id, [message])
                except Exception as e:
                    logger.error(f"Lỗi gửi sự kiện Pusher: {str(e)}")
            return message
        except Exception as e:
            logger.error(f"Lỗi không mong muốn: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")