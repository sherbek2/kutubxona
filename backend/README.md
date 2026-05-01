# Kutubxona Backend API

O'zbekistondagi eng yirik onlayn kutubxona platformasi backend API.

## Features

- ✅ User authentication & authorization (JWT)
- ✅ Book CRUD operations
- ✅ Store management system
- ✅ Review & rating system
- ✅ Messaging system
- ✅ File upload (Cloudinary)
- ✅ Search & filtering
- ✅ Map integration
- ✅ Favorites system
- ✅ Notifications
- ✅ Admin panel
- ✅ Reports system

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy (async)
- **Authentication**: JWT tokens
- **File Storage**: Cloudinary
- **Cache**: Redis
- **Task Queue**: Celery
- **API Documentation**: Swagger/OpenAPI

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Cloudinary account

### Setup

1. Clone the repository:
```bash
git clone https://github.com/sherbek2/kutubxona.git
cd kutubxona/backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Environment setup:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Database setup:
```bash
# Create database
createdb kutubxona

# Run migrations
alembic upgrade head
```

6. Start the server:
```bash
uvicorn app.main:app --reload
```

## Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/kutubxona

# Redis
REDIS_URL=redis://localhost:6379

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - User logout

### Users
- `GET /api/v1/users/me` - Get current user info
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/{user_id}` - Get user by ID

### Books
- `GET /api/v1/books` - Get books with filters
- `POST /api/v1/books` - Create new book
- `GET /api/v1/books/{book_id}` - Get book by ID
- `PUT /api/v1/books/{book_id}` - Update book
- `DELETE /api/v1/books/{book_id}` - Delete book

### Stores
- `GET /api/v1/stores` - Get stores with filters
- `POST /api/v1/stores` - Create new store
- `GET /api/v1/stores/{store_id}` - Get store by ID
- `PUT /api/v1/stores/{store_id}` - Update store

### Reviews
- `GET /api/v1/reviews` - Get reviews for item
- `POST /api/v1/reviews` - Create review
- `PUT /api/v1/reviews/{review_id}` - Update review
- `DELETE /api/v1/reviews/{review_id}` - Delete review

### Messages
- `GET /api/v1/messages/conversations` - Get user conversations
- `POST /api/v1/messages/conversations/{id}/messages` - Send message
- `GET /api/v1/messages/conversations/{id}/messages` - Get conversation messages

### Search
- `GET /api/v1/search` - Search books and stores
- `GET /api/v1/search/suggestions` - Get search suggestions

### Map
- `GET /api/v1/map/items` - Get nearby items
- `GET /api/v1/map/books/{id}/location` - Get book location
- `GET /api/v1/map/stores/{id}/location` - Get store location

## Database Schema

The application uses the following main tables:

- `users` - User information
- `books` - Book listings
- `stores` - Physical bookstores
- `categories` - Book categories
- `reviews` - User reviews
- `messages` - User messages
- `notifications` - User notifications
- `favorites` - User favorites
- `reports` - User reports

## Deployment

### Docker

Build and run with Docker:
```bash
docker build -t kutubxona-backend .
docker run -p 8000:8000 kutubxona-backend
```

### Production

For production deployment:

1. Set environment variables
2. Use PostgreSQL and Redis
3. Configure Cloudinary
4. Set up proper CORS
5. Use HTTPS
6. Configure proper logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
