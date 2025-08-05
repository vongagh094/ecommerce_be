from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.features.messages.schemas.MessageDTO import MessageCreateDTO, MessageResponseDTO, MessageUpdateDTO
from app.core.container import Container
from dependency_injector.wiring import inject, Provide
from app.features.messages.services.message_service import MessageService

router = APIRouter()

@router.post("/send", response_model=MessageResponseDTO, operation_id="sendMessage")
@inject
async def create_message(
    data: MessageCreateDTO,
    message_service: MessageService = Depends(Provide[Container.message_service])
):
    try:
        message = message_service.create_message(data)
        return message
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})

@router.post("/update-or-create", response_model=MessageResponseDTO | dict, operation_id="createOrUpdateMessage")
@inject
async def create_or_update_message(
    data: MessageCreateDTO,
    message_service: MessageService = Depends(Provide[Container.message_service])
):
    try:
        result = message_service.create_or_update_message(data)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})

@router.get("/list/{conversation_id}", response_model=List[MessageResponseDTO], operation_id="listMessagesByConversation")
@inject
async def get_messages(
    conversation_id: int,
    user_id: int,
    limit: int = 10,
    offset: int = 0,
    message_service: MessageService = Depends(Provide[Container.message_service])
):
    try:
        messages = message_service.get_messages(conversation_id, user_id, limit, offset)
        return messages
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})

@router.put("/update/{message_id}", response_model=MessageResponseDTO, operation_id="updateMessageReadStatus")
@inject
async def update_message(
    message_id: int,
    data: MessageUpdateDTO,
    message_service: MessageService = Depends(Provide[Container.message_service])
):
    try:
        message = message_service.update_message(message_id, data)
        if message is None:
            raise HTTPException(status_code=404, detail={"detail": "Message not found"})
        return message
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})