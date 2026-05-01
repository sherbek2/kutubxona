# Backend Implementation Prompt - Kutubxona Platformasi

## Kerakli Backend Implementation

Quyidagi backendni to'liq qiling, barcha funksiyalar bilan ishlaydigan, production-ready holatda bo'lishi kerak.

### Texnologik Stack
- **FastAPI** (Python 3.9+)
- **PostgreSQL** (14+)
- **SQLAlchemy 2.0** (async)
- **Alembic** (migrations)
- **Redis** (cache va sessions)
- **Cloudinary** (image storage)
- **JWT** (authentication)
- **Pydantic** (validation)
- **pytest** (testing)

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py              # Configuration
│   ├── database.py            # Database connection
│   ├── dependencies.py        # Dependencies
│   │
│   ├── models/                # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── store.py
│   │   ├── review.py
│   │   ├── message.py
│   │   ├── notification.py
│   │   └── base.py
│   │
│   ├── schemas/               # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── store.py
│   │   ├── review.py
│   │   ├── message.py
│   │   ├── notification.py
│   │   └── common.py
│   │
│   ├── api/                   # API routes
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── books.py
│   │   │   ├── stores.py
│   │   │   ├── reviews.py
│   │   │   ├── messages.py
│   │   │   ├── notifications.py
│   │   │   ├── map.py
│   │   │   ├── search.py
│   │   │   ├── categories.py
│   │   │   ├── favorites.py
│   │   │   ├── reports.py
│   │   │   └── admin.py
│   │   └── deps.py
│   │
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── security.py        # JWT, password hashing
│   │   ├── config.py          # Settings
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── middleware.py      # Custom middleware
│   │
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── book_service.py
│   │   ├── store_service.py
│   │   ├── review_service.py
│   │   ├── message_service.py
│   │   ├── notification_service.py
│   │   ├── email_service.py
│   │   ├── upload_service.py
│   │   └── search_service.py
│   │
│   ├── utils/                 # Utilities
│   │   ├── __init__.py
│   │   ├── email.py
│   │   ├── image.py
│   │   ├── location.py
│   │   ├── pagination.py
│   │   └── validators.py
│   │
│   └── tests/                 # Tests
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_users.py
│       ├── test_books.py
│       ├── test_stores.py
│       └── test_utils.py
│
├── alembic/                   # Database migrations
│   ├── versions/
│   ├── env.py
│   └── alembic.ini
│
├── requirements.txt           # Dependencies
├── .env.example              # Environment variables
├── docker-compose.yml        # Docker setup
├── Dockerfile                # Docker image
└── README.md                 # Documentation
```

---

## Implementation Requirements

### 1. Core Setup

#### 1.1 FastAPI Application
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, users, books, stores, reviews, messages, notifications, map, search, categories, favorites, reports, admin
from app.core.config import settings

app = FastAPI(
    title="Kutubxona API",
    description="O'zbekistondagi eng yirik onlayn kutubxona platformasi",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(books.router, prefix="/api/v1/books", tags=["Books"])
app.include_router(stores.router, prefix="/api/v1/stores", tags=["Stores"])
# ... boshqa routerlar
```

#### 1.2 Configuration
```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    
    # Email
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    
    # App settings
    ALLOWED_HOSTS: list = ["*"]
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 2. Database Models

#### 2.1 Base Model
```python
# app/models/base.py
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

#### 2.2 User Model
```python
# app/models/user.py
from sqlalchemy import Column, String, Boolean, DECIMAL, Integer, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    avatar_url = Column(String(500))
    bio = Column(Text)
    location = Column(String(200))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_blocked = Column(Boolean, default=False)
    role = Column(String(20), default="user")
    rating = Column(DECIMAL(3, 2), default=0.00)
    total_reviews = Column(Integer, default=0)
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    books = relationship("Book", back_populates="seller")
    stores = relationship("Store", back_populates="owner")
    reviews = relationship("Review", back_populates="reviewer")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    notifications = relationship("Notification", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
```

#### 2.3 Book Model
```python
# app/models/book.py
from sqlalchemy import Column, String, Integer, DECIMAL, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Book(BaseModel):
    __tablename__ = "books"
    
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    language = Column(String(50), nullable=False)
    year = Column(Integer)
    pages = Column(Integer)
    isbn = Column(String(20))
    condition = Column(String(20), default="new")
    type = Column(String(20), nullable=False)  # sell, free, rent
    price = Column(Integer)
    rent_price = Column(Integer)
    rent_duration = Column(String(20))
    location = Column(String(200))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="active")
    is_featured = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    contact_count = Column(Integer, default=0)
    expires_at = Column(DateTime(timezone=True))
    
    # Relationships
    seller = relationship("User", back_populates="books")
    category = relationship("Category")
    images = relationship("BookImage", back_populates="book")
    reviews = relationship("Review", back_populates="book")
    favorites = relationship("Favorite", back_populates="book")
```

### 3. Pydantic Schemas

#### 3.1 User Schemas
```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    bio: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class UserResponse(UserBase):
    id: int
    avatar_url: Optional[str] = None
    rating: float
    total_reviews: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
```

#### 3.2 Book Schemas
```python
# app/schemas/book.py
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    description: str
    category_id: Optional[int] = None
    language: str
    year: Optional[int] = None
    pages: Optional[int] = None
    isbn: Optional[str] = None
    condition: str = "new"
    type: str  # sell, free, rent
    price: Optional[int] = None
    rent_price: Optional[int] = None
    rent_duration: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class BookCreate(BookBase):
    images: Optional[List[str]] = []
    
    @validator('type')
    def validate_type(cls, v):
        if v not in ['sell', 'free', 'rent']:
            raise ValueError('Type must be sell, free, or rent')
        return v
    
    @validator('price')
    def validate_price(cls, v, values):
        if values.get('type') == 'sell' and (not v or v <= 0):
            raise ValueError('Price is required for sell type')
        return v

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    status: Optional[str] = None

class BookResponse(BookBase):
    id: int
    seller_id: int
    status: str
    is_featured: bool
    view_count: int
    like_count: int
    contact_count: int
    created_at: datetime
    updated_at: datetime
    seller: Optional[dict] = None
    category: Optional[dict] = None
    images: List[str] = []
    distance: Optional[float] = None
    
    class Config:
        from_attributes = True

class BookListResponse(BaseModel):
    books: List[BookResponse]
    pagination: dict
```

### 4. API Routes

#### 4.1 Authentication
```python
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.auth_service import AuthService
from app.core.security import create_access_token, create_refresh_token

router = APIRouter()

@router.post("/register", response_model=dict)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    user = await auth_service.register(user_data)
    
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=dict)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    user = await auth_service.authenticate(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
```

#### 4.2 Books API
```python
# app/api/v1/books.py
from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app.schemas.book import BookCreate, BookResponse, BookListResponse
from app.services.book_service import BookService
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=BookListResponse)
async def get_books(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    type: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius: Optional[int] = Query(10, ge=1, le=100),
    sort: Optional[str] = Query("created_at"),
    order: Optional[str] = Query("desc"),
    db: AsyncSession = Depends(get_db)
):
    book_service = BookService(db)
    books, pagination = await book_service.get_books(
        page=page,
        limit=limit,
        search=search,
        category=category,
        type=type,
        min_price=min_price,
        max_price=max_price,
        lat=lat,
        lng=lng,
        radius=radius,
        sort=sort,
        order=order
    )
    
    return BookListResponse(
        books=books,
        pagination=pagination
    )

@router.post("/", response_model=BookResponse)
async def create_book(
    book_data: BookCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    book_service = BookService(db)
    book = await book_service.create_book(book_data, current_user.id)
    return book

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    book_service = BookService(db)
    book = await book_service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/{book_id}/images")
async def upload_book_images(
    book_id: int,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    book_service = BookService(db)
    images = await book_service.upload_images(book_id, files, current_user.id)
    return {"images": images}
```

### 5. Services

#### 5.1 Book Service
```python
# app/services/book_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from app.models.book import Book
from app.models.user import User
from app.schemas.book import BookCreate
from app.utils.pagination import paginate
from app.utils.location import calculate_distance
from typing import List, Tuple, Optional

class BookService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_books(
        self,
        page: int = 1,
        limit: int = 20,
        search: Optional[str] = None,
        category: Optional[str] = None,
        type: Optional[str] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius: Optional[int] = None,
        sort: str = "created_at",
        order: str = "desc"
    ) -> Tuple[List[Book], dict]:
        
        query = select(Book).where(Book.status == "active")
        
        # Search filter
        if search:
            search_filter = or_(
                Book.title.ilike(f"%{search}%"),
                Book.author.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        # Category filter
        if category:
            query = query.join(Book.category).where(Category.name == category)
        
        # Type filter
        if type:
            query = query.where(Book.type == type)
        
        # Price filter
        if min_price is not None:
            query = query.where(Book.price >= min_price)
        if max_price is not None:
            query = query.where(Book.price <= max_price)
        
        # Location filter
        if lat and lng and radius:
            # Haversine formula for distance calculation
            distance_formula = func.acos(
                func.cos(func.radians(lat)) * 
                func.cos(func.radians(Book.latitude)) * 
                func.cos(func.radians(Book.longitude) - func.radians(lng)) + 
                func.sin(func.radians(lat)) * 
                func.sin(func.radians(Book.latitude))
            ) * 6371
            
            query = query.where(distance_formula <= radius)
        
        # Sorting
        if sort == "created_at":
            query = query.order_by(Book.created_at.desc() if order == "desc" else Book.created_at.asc())
        elif sort == "price":
            query = query.order_by(Book.price.desc() if order == "desc" else Book.price.asc())
        elif sort == "title":
            query = query.order_by(Book.title.desc() if order == "desc" else Book.title.asc())
        
        # Pagination
        result = await paginate(self.db, query, page, limit)
        
        # Add distance if location is provided
        if lat and lng:
            for book in result.items:
                if book.latitude and book.longitude:
                    book.distance = calculate_distance(lat, lng, book.latitude, book.longitude)
        
        return result.items, result.pagination
    
    async def create_book(self, book_data: BookCreate, user_id: int) -> Book:
        book = Book(**book_data.dict(), seller_id=user_id)
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)
        return book
    
    async def get_book(self, book_id: int) -> Optional[Book]:
        query = select(Book).where(Book.id == book_id, Book.status == "active")
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def upload_images(self, book_id: int, files: List[UploadFile], user_id: int) -> List[str]:
        # Verify book ownership
        book = await self.get_book(book_id)
        if not book or book.seller_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        # Upload images to Cloudinary
        from app.services.upload_service import UploadService
        upload_service = UploadService()
        
        image_urls = []
        for file in files:
            url = await upload_service.upload_image(file, "books")
            image_urls.append(url)
        
        # Save to database
        for i, url in enumerate(image_urls):
            book_image = BookImage(
                book_id=book_id,
                image_url=url,
                sort_order=i,
                is_primary=(i == 0)
            )
            self.db.add(book_image)
        
        await self.db.commit()
        return image_urls
```

### 6. Security

#### 6.1 JWT Authentication
```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
```

### 7. Database Setup

#### 7.1 Database Connection
```python
# app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### 8. Testing

#### 8.1 Test Configuration
```python
# app/tests/conftest.py
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models.base import Base

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://test_user:test_password@localhost/test_kutubxona"

@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def test_session(test_engine):
    TestSessionLocal = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with TestSessionLocal() as session:
        yield session

@pytest.fixture
async def client(test_session):
    app.dependency_overrides[get_db] = lambda: test_session
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

### 9. Docker Configuration

#### 9.1 Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 9.2 Docker Compose
```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: kutubxona
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

  backend:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:password@db/kutubxona
      REDIS_URL: redis://redis:6379
    volumes:
      - .:/app

volumes:
  postgres_data:
```

### 10. Requirements

```txt
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
asyncpg==0.29.0
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
cloudinary==1.38.0
redis==5.0.1
celery==5.3.4
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.21.1
python-dotenv==1.0.0
```

---

## Implementation Qadamlari

1. **Project Setup**: Barcha papkalarni va fayllarni yarating
2. **Database Models**: Barcha modellarni yarating
3. **Migrations**: Alembic migrationlarni yarating
4. **Schemas**: Pydantic schemalarni yarating
5. **Services**: Business logic servislarni yarating
6. **API Routes**: Barcha API endpointlarni yarating
7. **Authentication**: JWT auth sistemini yarating
8. **File Upload**: Cloudinary integratsiyasi
9. **Testing**: Unit va integration testlar
10. **Docker**: Docker konfiguratsiyasi
11. **Documentation**: Swagger/OpenAPI dokumentatsiyasi

---

## Qo'shimcha Talablar

- Barcha API endpointlar bo'lishi kerak
- Error handling bo'lishi kerak
- Logging bo'lishi kerak
- Rate limiting bo'lishi kerak
- Input validation bo'lishi kerak
- Database transactions bo'lishi kerak
- Async/await pattern ishlatilishi kerak
- Type hints ishlatilishi kerak
- Docstrings bo'lishi kerak
- Production-ready bo'lishi kerak

Backendni to'liq ishlaydigan holatda yarating, barcha funksiyalar bilan!
