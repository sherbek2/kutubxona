from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, users, books, stores, reviews, messages, notifications, map, search, categories, favorites, reports, admin
from app.core.config import settings

app = FastAPI(
    title="Kutubxona API",
    description="O'zbekistondagi eng yirik onlayn kutubxona platformasi",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["Reviews"])
app.include_router(messages.router, prefix="/api/v1/messages", tags=["Messages"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["Notifications"])
app.include_router(map.router, prefix="/api/v1/map", tags=["Map"])
app.include_router(search.router, prefix="/api/v1/search", tags=["Search"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(favorites.router, prefix="/api/v1/favorites", tags=["Favorites"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {
        "message": "Kutubxona API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
