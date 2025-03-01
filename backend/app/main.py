from fastapi import FastAPI
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.code import router as code_router
from app.api.v1.endpoints.websocket import router as websocket_router
from app.api.v1.endpoints.room import router as room_router
from app.api.v1.endpoints.ai import router as ai_router
from app.core.database import engine, Base

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Include the auth router
app.include_router(auth_router, prefix="/api/v1")
app.include_router(code_router, prefix="/api/v1")
app.include_router(websocket_router, prefix="/api/v1")
app.include_router(room_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")