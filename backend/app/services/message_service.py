from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from app.models.message import Conversation, ConversationParticipant, Message
from app.models.user import User
from app.schemas.message import MessageCreate
from typing import List, Tuple

class MessageService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_conversation(self, user_id: int, participant_id: int) -> Conversation:
        # Check if conversation already exists
        result = await self.db.execute(
            select(Conversation)
            .join(ConversationParticipant)
            .where(
                and_(
                    ConversationParticipant.user_id.in_([user_id, participant_id])
                )
            )
            .group_by(Conversation.id)
            .having(func.count(ConversationParticipant.user_id) == 2)
        )
        existing_conversation = result.scalar_one_or_none()
        
        if existing_conversation:
            return existing_conversation
        
        # Create new conversation
        conversation = Conversation()
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        
        # Add participants
        participant1 = ConversationParticipant(
            conversation_id=conversation.id,
            user_id=user_id
        )
        participant2 = ConversationParticipant(
            conversation_id=conversation.id,
            user_id=participant_id
        )
        
        self.db.add(participant1)
        self.db.add(participant2)
        await self.db.commit()
        
        return conversation
    
    async def get_user_conversations(self, user_id: int) -> List[Conversation]:
        result = await self.db.execute(
            select(Conversation)
            .join(ConversationParticipant)
            .where(ConversationParticipant.user_id == user_id)
            .options(
                selectinload(Conversation.participants),
                selectinload(Conversation.messages)
            )
            .order_by(Conversation.updated_at.desc())
        )
        conversations = result.scalars().all()
        return conversations
    
    async def get_conversation_messages(
        self,
        conversation_id: int,
        user_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[Message]:
        # Check if user is participant
        result = await self.db.execute(
            select(ConversationParticipant).where(
                and_(
                    ConversationParticipant.conversation_id == conversation_id,
                    ConversationParticipant.user_id == user_id
                )
            )
        )
        participant = result.scalar_one_or_none()
        
        if not participant:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not a participant in this conversation"
            )
        
        # Get messages
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .options(selectinload(Message.sender))
            .order_by(Message.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        messages = result.scalars().all()
        return messages
    
    async def send_message(
        self,
        conversation_id: int,
        user_id: int,
        message_data: MessageCreate
    ) -> Message:
        # Check if user is participant
        result = await self.db.execute(
            select(ConversationParticipant).where(
                and_(
                    ConversationParticipant.conversation_id == conversation_id,
                    ConversationParticipant.user_id == user_id
                )
            )
        )
        participant = result.scalar_one_or_none()
        
        if not participant:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not a participant in this conversation"
            )
        
        # Create message
        message = Message(
            conversation_id=conversation_id,
            sender_id=user_id,
            content=message_data.content,
            type=message_data.type,
            file_url=message_data.file_url
        )
        
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        
        return message
    
    async def mark_message_as_read(self, message_id: int, user_id: int):
        result = await self.db.execute(
            select(Message).where(Message.id == message_id)
        )
        message = result.scalar_one_or_none()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        # Update participant's last_read_at
        await self.db.execute(
            select(ConversationParticipant).where(
                and_(
                    ConversationParticipant.conversation_id == message.conversation_id,
                    ConversationParticipant.user_id == user_id
                )
            )
        )
        
        # Mark message as read if not sender
        if message.sender_id != user_id:
            message.is_read = True
            message.read_at = func.now()
            await self.db.commit()
