from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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


# origins = [
#     "http://localhost:5173",  # Or your frontend's origin
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the auth router
app.include_router(auth_router, prefix="/api/v1")
app.include_router(code_router, prefix="/api/v1")
app.include_router(websocket_router, prefix="/api/v1")
app.include_router(room_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")