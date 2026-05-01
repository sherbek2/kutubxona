from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash, verify_password, verify_token

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def register(self, user_data: UserCreate) -> UserResponse:
        # Check if user already exists
        result = await self.db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if phone already exists
        result = await self.db.execute(
            select(User).where(User.phone == user_data.phone)
        )
        existing_phone = result.scalar_one_or_none()
        
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=hashed_password,
            location=user_data.location,
            latitude=user_data.latitude,
            longitude=user_data.longitude,
            bio=user_data.bio
        )
        
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        
        return UserResponse.from_orm(db_user)
    
    async def authenticate(self, email: str, password: str) -> UserResponse:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.password_hash):
            return None
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account is deactivated"
            )
        
        return UserResponse.from_orm(user)
    
    async def refresh_token(self, refresh_token: str) -> UserResponse:
        try:
            email = verify_token(refresh_token)
            result = await self.db.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            
            if not user or not user.is_active:
                return None
            
            return UserResponse.from_orm(user)
        except:
            return None
    
    async def logout(self, refresh_token: str):
        # In a real implementation, you would revoke the refresh token
        # For now, we'll just return success
        pass
