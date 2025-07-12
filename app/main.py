from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.auth.controller import router as auth_router
from app.core.config import settings
from app.core.database import Base, engine
from app.feedback.controller import router as feedback_router
from app.role.controller import router as role_router
from app.user.controller import router as user_router

# Create tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(role_router, prefix="/admin", tags=["Role"])
app.include_router(feedback_router, tags=["Feedback"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to Feedback Collector API"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
