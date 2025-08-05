from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.features.messages.schemas.ConversationDTO import ConversationCreateDTO, ConversationResponseDTO
from app.core.container import Container
from dependency_injector.wiring import inject, Provide
from app.features.messages.services.message_service import MessageService

router = APIRouter()

@router.post("/create", response_model=ConversationResponseDTO, operation_id="createConversation")
@inject
async def create_conversation(
    data: ConversationCreateDTO,
    message_service: MessageService = Depends(Provide[Container.message_service])
):
    try:
        conversation = message_service.create_conversation(data)
        return conversation
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})

@router.get("/list/{user_id}", response_model=List[ConversationResponseDTO], operation_id="listConversationsByUser")
@inject
async def get_conversations_by_user(
    user_id: int,
    message_service: MessageService = Depends(Provide[Container.message_service])
):
    try:
        conversations = message_service.get_conversations_by_user(user_id)
        return conversations
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})

@router.get("/list/property/{property_id}", response_model=List[ConversationResponseDTO], operation_id="listConversationsByProperty")
@inject
async def get_conversations_by_property(
    property_id: int,
    message_service: MessageService = Depends(Provide[Container.message_service])
):
    try:
        conversations = message_service.get_conversations_by_property(property_id)
        return conversations
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"detail": f"Internal server error: {str(e)}"})