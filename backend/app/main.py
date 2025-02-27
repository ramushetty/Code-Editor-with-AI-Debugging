from fastapi import FastAPI
from app.api.v1.endpoints.auth import router as auth_router
from app.core.database import engine, Base

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Include the auth router
app.include_router(auth_router, prefix="/api/v1")