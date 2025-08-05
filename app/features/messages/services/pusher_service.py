from pusher import Pusher
from app.features.messages.schemas.PusherDTO import PusherConfigResponse
from app.features.messages.schemas.MessageDTO import MessageResponseDTO
from app.features.messages.core.settings import get_settings
from fastapi import HTTPException
import logging
from typing import List

logger = logging.getLogger(__name__)

class PusherService:
    def __init__(self, pusher: Pusher):
        self.pusher = pusher
        self.config = get_settings()
        logger.info("Khởi tạo PusherService thành công")

    def get_pusher_config(self) -> PusherConfigResponse:
        logger.info("Nhận yêu cầu lấy cấu hình Pusher")
        try:
            return PusherConfigResponse(
                app_key=self.config["NEXT_PUBLIC_PUSHER_KEY"],
                cluster=self.config["NEXT_PUBLIC_PUSHER_CLUSTER"]
            )
        except Exception as e:
            logger.error(f"Lỗi khi lấy cấu hình Pusher: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ: {str(e)}")

    def trigger_new_message(self, conversation_id: int, message: MessageResponseDTO) -> None:
        try:
            logger.info(f"Gửi sự kiện new-message cho conversation-{conversation_id}")
            # Use model_dump with mode='json' to serialize datetime fields correctly
            self.pusher.trigger(f"conversation-{conversation_id}", "new-message", message.model_dump(mode='json'))
        except Exception as e:
            logger.error(f"Lỗi gửi sự kiện new-message: {str(e)}")
            raise e

    def trigger_messages_read(self, conversation_id: int, messages: List[MessageResponseDTO]) -> None:
        try:
            logger.info(f"Gửi sự kiện messages-read cho conversation-{conversation_id}")
            # Serialize each message with mode='json' to handle datetime fields
            message_list = [msg.model_dump(mode='json') for msg in messages]
            self.pusher.trigger(f"conversation-{conversation_id}", "messages-read", message_list)
        except Exception as e:
            logger.error(f"Lỗi gửi sự kiện messages-read: {str(e)}")
            raise e