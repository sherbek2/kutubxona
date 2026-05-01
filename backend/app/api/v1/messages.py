from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app.schemas.message import MessageCreate, MessageResponse, ConversationResponse
from app.services.message_service import MessageService
from app.core.security import get_current_user

router = APIRouter()

@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    message_service = MessageService(db)
    conversations = await message_service.get_user_conversations(current_user["id"])
    return [ConversationResponse.from_orm(conv) for conv in conversations]

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    message_service = MessageService(db)
    messages = await message_service.get_conversation_messages(
        conversation_id, current_user["id"], skip, limit
    )
    return [MessageResponse.from_orm(msg) for msg in messages]

@router.post("/conversations", response_model=ConversationResponse)
async def create_conversation(
    participant_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    message_service = MessageService(db)
    conversation = await message_service.create_conversation(
        current_user["id"], participant_id
    )
    return ConversationResponse.from_orm(conversation)

@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
async def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    message_service = MessageService(db)
    message = await message_service.send_message(
        conversation_id, current_user["id"], message_data
    )
    return MessageResponse.from_orm(message)

@router.put("/messages/{message_id}/read")
async def mark_message_as_read(
    message_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    message_service = MessageService(db)
    await message_service.mark_message_as_read(message_id, current_user["id"])
    return {"message": "Message marked as read"}
