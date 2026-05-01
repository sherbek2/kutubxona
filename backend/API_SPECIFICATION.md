# Kutubxona Platformasi - Backend API Specification

## Texnologik Stack

- **Backend Framework**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (JSON Web Tokens)
- **File Storage**: Cloudinary (rasm uchun)
- **Cache**: Redis (sesions va cache uchun)
- **API Documentation**: Swagger/OpenAPI (FastAPI avtomatik)

## API Base URL

```
Development: http://localhost:8000/api/v1
Production: https://api.kutubxona.uz/v1
```

## Authentication

Barcha protected endpointlarda JWT token kerak:
```
Authorization: Bearer <jwt_token>
```

## Response Format

Barcha response lar bir xil formatda:
```json
{
  "success": true,
  "data": {},
  "message": "Success message",
  "errors": null
}
```

Error response:
```json
{
  "success": false,
  "data": null,
  "message": "Error message",
  "errors": {
    "field": ["Error message"]
  }
}
```

---

## 1. Authentication Endpoints

### 1.1 Register (Ro'yxatdan o'tish)
```
POST /auth/register
```

**Request Body:**
```json
{
  "first_name": "Ali",
  "last_name": "Karimov",
  "email": "ali@example.com",
  "phone": "+998901234567",
  "password": "password123",
  "location": "Toshkent, Chilonzor",
  "latitude": 41.3111,
  "longitude": 69.2797
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "first_name": "Ali",
      "last_name": "Karimov",
      "email": "ali@example.com",
      "phone": "+998901234567",
      "location": "Toshkent, Chilonzor",
      "avatar": null,
      "created_at": "2024-01-15T10:30:00Z"
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "expires_in": 3600
  },
  "message": "User successfully registered"
}
```

### 1.2 Login (Kirish)
```
POST /auth/login
```

**Request Body:**
```json
{
  "email": "ali@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": 1,
      "first_name": "Ali",
      "last_name": "Karimov",
      "email": "ali@example.com",
      "avatar": "https://res.cloudinary.com/..."
    },
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "expires_in": 3600
  },
  "message": "Login successful"
}
```

### 1.3 Refresh Token
```
POST /auth/refresh
```

**Headers:**
```
Authorization: Bearer <refresh_token>
```

### 1.4 Logout (Chiqish)
```
POST /auth/logout
```

**Headers:**
```
Authorization: Bearer <access_token>
```

---

## 2. User Profile Endpoints

### 2.1 Get Current User Profile
```
GET /users/me
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "first_name": "Ali",
    "last_name": "Karimov",
    "email": "ali@example.com",
    "phone": "+998901234567",
    "location": "Toshkent, Chilonzor",
    "latitude": 41.3111,
    "longitude": 69.2797,
    "avatar": "https://res.cloudinary.com/...",
    "bio": "Kitoblarni yaxshi ko'raman",
    "rating": 4.8,
    "created_at": "2024-01-15T10:30:00Z",
    "stats": {
      "total_books": 12,
      "active_books": 8,
      "total_stores": 2,
      "followers": 156
    }
  }
}
```

### 2.2 Update User Profile
```
PUT /users/me
```

**Request Body:**
```json
{
  "first_name": "Ali",
  "last_name": "Karimov",
  "phone": "+998901234567",
  "location": "Toshkent, Chilonzor",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "bio": "Kitoblarni yaxshi ko'raman"
}
```

### 2.3 Upload Avatar
```
POST /users/me/avatar
```

**Request:** multipart/form-data
```
file: <image_file>
```

### 2.4 Change Password
```
PUT /users/me/password
```

**Request Body:**
```json
{
  "current_password": "old_password",
  "new_password": "new_password"
}
```

---

## 3. Books Endpoints

### 3.1 Get Books (Kitoblarni olish)
```
GET /books
```

**Query Parameters:**
- `page`: int (default: 1)
- `limit`: int (default: 20, max: 100)
- `search`: string (kitob yoki muallif nomi bo'yicha qidirish)
- `category`: string (kategoriya bo'yicha filter)
- `type`: string (sell, free, rent)
- `min_price`: int (minimal narx)
- `max_price`: int (maksimal narx)
- `lat`: float (latitude)
- `lng`: float (longitude)
- `radius`: int (radius km, default: 10)
- `sort`: string (created_at, price, title, distance)
- `order`: string (asc, desc)

**Response:**
```json
{
  "success": true,
  "data": {
    "books": [
      {
        "id": 1,
        "title": "Alkimyogar",
        "author": "Paulo Koelyo",
        "description": "Sarguzasht romani...",
        "category": "Badiiy adabiyot",
        "language": "O'zbekcha",
        "year": 2020,
        "pages": 208,
        "condition": "like_new",
        "type": "sell",
        "price": 45000,
        "rent_price": null,
        "rent_duration": null,
        "location": "Toshkent, Chilonzor",
        "latitude": 41.3111,
        "longitude": 69.2797,
        "distance": 2.5,
        "images": [
          "https://res.cloudinary.com/..."
        ],
        "seller": {
          "id": 1,
          "first_name": "Ali",
          "last_name": "Karimov",
          "avatar": "https://res.cloudinary.com/...",
          "rating": 4.8
        },
        "stats": {
          "views": 156,
          "likes": 23,
          "created_at": "2024-04-15T10:30:00Z"
        }
      }
    ],
    "pagination": {
      "current_page": 1,
      "total_pages": 10,
      "total_items": 200,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

### 3.2 Get Book by ID
```
GET /books/{book_id}
```

**Response:** Kitob haqida to'liq ma'lumot

### 3.3 Create Book (Yangi e'lon)
```
POST /books
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "title": "Alkimyogar",
  "author": "Paulo Koelyo",
  "description": "Sarguzasht romani...",
  "category": "Badiiy adabiyot",
  "language": "O'zbekcha",
  "year": 2020,
  "pages": 208,
  "condition": "like_new",
  "type": "sell",
  "price": 45000,
  "rent_price": null,
  "rent_duration": null,
  "location": "Toshkent, Chilonzor",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "images": [
    "https://res.cloudinary.com/..."
  ]
}
```

### 3.4 Update Book
```
PUT /books/{book_id}
```

**Headers:**
```
Authorization: Bearer <access_token>
```

### 3.5 Delete Book
```
DELETE /books/{book_id}
```

**Headers:**
```
Authorization: Bearer <access_token>
```

### 3.6 Upload Book Images
```
POST /books/{book_id}/images
```

**Request:** multipart/form-data
```
files: [<image_file1>, <image_file2>]
```

### 3.7 Like/Unlike Book
```
POST /books/{book_id}/like
```

### 3.8 Get User Books
```
GET /users/me/books
```

---

## 4. Stores Endpoints

### 4.1 Get Stores
```
GET /stores
```

**Query Parameters:**
- `page`: int
- `limit`: int
- `search`: string
- `category`: string
- `lat`: float
- `lng`: float
- `radius`: int

### 4.2 Get Store by ID
```
GET /stores/{store_id}
```

### 4.3 Create Store
```
POST /stores
```

**Request Body:**
```json
{
  "name": "Chilonzor kitob do'koni",
  "category": "bookstore",
  "description": "Katta kitob do'koni...",
  "address": "Toshkent, Chilonzor, Bunyodkor 45",
  "latitude": 41.3111,
  "longitude": 69.2797,
  "phone": "+998901234567",
  "email": "info@store.uz",
  "website": "https://store.uz",
  "facebook": "storepage",
  "instagram": "@store",
  "open_hours": {
    "monday": {"open": "09:00", "close": "18:00", "closed": false},
    "tuesday": {"open": "09:00", "close": "18:00", "closed": false},
    "wednesday": {"open": "09:00", "close": "18:00", "closed": false},
    "thursday": {"open": "09:00", "close": "18:00", "closed": false},
    "friday": {"open": "09:00", "close": "18:00", "closed": false},
    "saturday": {"open": "10:00", "close": "16:00", "closed": false},
    "sunday": {"open": "", "close": "", "closed": true}
  },
  "features": ["Wi-Fi", "Parking", "Bolalar uchun bo'lim"],
  "images": [
    "https://res.cloudinary.com/..."
  ]
}
```

### 4.4 Update Store
```
PUT /stores/{store_id}
```

### 4.5 Delete Store
```
DELETE /stores/{store_id}
```

### 4.6 Get Store Books
```
GET /stores/{store_id}/books
```

### 4.7 Add Book to Store
```
POST /stores/{store_id}/books
```

**Request Body:**
```json
{
  "title": "Alkimyogar",
  "author": "Paulo Koelyo",
  "price": 45000,
  "stock": 15,
  "category": "Badiiy adabiyot",
  "description": "...",
  "image": "https://res.cloudinary.com/..."
}
```

---

## 5. Map & Location Endpoints

### 5.1 Get Nearby Items
```
GET /map/nearby
```

**Query Parameters:**
- `lat`: float (required)
- `lng`: float (required)
- `radius`: int (default: 10 km)
- `type`: string (books, stores, all)
- `book_type`: string (sell, free, rent)

**Response:**
```json
{
  "success": true,
  "data": {
    "books": [
      {
        "id": 1,
        "title": "Alkimyogar",
        "type": "sell",
        "price": 45000,
        "location": [41.3111, 69.2797],
        "address": "Toshkent, Chilonzor",
        "distance": 2.5,
        "seller": "Ali Karimov"
      }
    ],
    "stores": [
      {
        "id": 1,
        "name": "Chilonzor kitob do'koni",
        "location": [41.3111, 69.2797],
        "address": "Toshkent, Chilonzor",
        "distance": 2.1,
        "books_count": 156,
        "rating": 4.8
      }
    ]
  }
}
```

### 5.2 Get Address from Coordinates
```
GET /map/reverse-geocode
```

**Query Parameters:**
- `lat`: float
- `lng`: float

### 5.3 Get Coordinates from Address
```
GET /map/geocode
```

**Query Parameters:**
- `address`: string

---

## 6. Reviews & Ratings Endpoints

### 6.1 Create Review
```
POST /reviews
```

**Request Body:**
```json
{
  "target_type": "book", // book, store
  "target_id": 1,
  "rating": 5,
  "comment": "Ajoyib kitob!"
}
```

### 6.2 Get Reviews
```
GET /reviews
```

**Query Parameters:**
- `target_type`: string
- `target_id`: int
- `page`: int
- `limit`: int

### 6.3 Update Review
```
PUT /reviews/{review_id}
```

### 6.4 Delete Review
```
DELETE /reviews/{review_id}
```

---

## 7. Messages & Chat Endpoints

### 7.1 Get Conversations
```
GET /messages/conversations
```

### 7.2 Get Messages
```
GET /messages/conversations/{conversation_id}
```

### 7.3 Send Message
```
POST /messages
```

**Request Body:**
```json
{
  "receiver_id": 2,
  "content": "Assalom alaykum, kitob hali sotuvdami?",
  "type": "text" // text, image
}
```

---

## 8. Notifications Endpoints

### 8.1 Get Notifications
```
GET /notifications
```

### 8.2 Mark as Read
```
PUT /notifications/{notification_id}/read
```

### 8.3 Mark All as Read
```
PUT /notifications/read-all
```

---

## 9. Search Endpoints

### 9.1 Global Search
```
GET /search
```

**Query Parameters:**
- `q`: string (search query)
- `type`: string (books, stores, users, all)
- `page`: int
- `limit`: int

---

## 10. Categories Endpoints

### 10.1 Get Categories
```
GET /categories
```

### 10.2 Get Category by ID
```
GET /categories/{category_id}
```

---

## 11. Favorites Endpoints

### 11.1 Get Favorites
```
GET /favorites
```

### 11.2 Add to Favorites
```
POST /favorites
```

**Request Body:**
```json
{
  "item_type": "book", // book, store
  "item_id": 1
}
```

### 11.3 Remove from Favorites
```
DELETE /favorites/{favorite_id}
```

---

## 12. Reports Endpoints

### 12.1 Create Report
```
POST /reports
```

**Request Body:**
```json
{
  "target_type": "book", // book, store, user
  "target_id": 1,
  "reason": "spam", // spam, inappropriate, fake, other
  "description": "Bu e'lon noto'g'ri ma'lumot"
}
```

---

## 13. Admin Endpoints

### 13.1 Get Dashboard Stats
```
GET /admin/dashboard
```

### 13.2 Get All Users
```
GET /admin/users
```

### 13.3 Block/Unblock User
```
PUT /admin/users/{user_id}/block
```

### 13.4 Get All Books
```
GET /admin/books
```

### 13.5 Approve/Reject Book
```
PUT /admin/books/{book_id}/status
```

---

## Error Codes

- `400`: Bad Request - Noto'g'ri so'rov
- `401`: Unauthorized - Avtorizatsiyadan o'tilmagan
- `403`: Forbidden - Ruxsat berilmagan
- `404`: Not Found - Topilmadi
- `409`: Conflict - Konflikt (masalan, email allaqachon mavjud)
- `422`: Unprocessable Entity - Validatsiya xatoligi
- `429`: Too Many Requests - Juda ko'p so'rovlar
- `500`: Internal Server Error - Server xatoligi

---

## Rate Limiting

- Guest users: 100 so'rov/soat
- Authenticated users: 1000 so'rov/soat
- Upload endpoints: 10 so'rov/soat

---

## WebSocket Events

Real-time uchun WebSocket:

### Connection
```
ws://localhost:8000/ws/{user_id}
```

### Events
- `new_message`: Yangi xabar
- `message_read`: Xabar o'qilgan
- `user_online`: User onlayn
- `user_offline`: User oflayn
- `notification`: Yangi bildirishnoma

---

## File Upload

- Max file size: 5MB
- Allowed formats: JPEG, PNG, GIF, WebP
- Images avtomatik ravishda optimizatsiya qilinadi
- Cloudinary orqali saqlanadi

---

## Security

- Barcha so'rovlar HTTPS orqali bo'lishi kerak
- JWT tokenlar 1 soat amal qiladi
- Refresh tokenlar 30 kun amal qiladi
- Passwordlar bcrypt orqali hashlanadi
- CORS sozlangan
- SQL injection va XSSdan himoya
