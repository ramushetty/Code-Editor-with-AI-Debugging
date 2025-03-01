from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.room import RoomCreate, RoomJoin
from app.services.room_service import create_room, join_room
from app.core.database import get_db
from app.core.security import get_current_user
from uuid import UUID

router = APIRouter()

@router.post("/rooms", response_model=RoomCreate)
def create_room_endpoint(db: Session = Depends(get_db)):
    try:
        return create_room(db)  # No code_file_id needed
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/rooms/join", response_model=RoomJoin)
def join_room_endpoint(room: RoomJoin, db: Session = Depends(get_db), current_user: UUID = Depends(get_current_user)):
    try:
        # Validate the room and add the user to the room
        db_room = join_room(db, room.room_number, current_user)
        return {"room_number": db_room.room_number, "users": [{"id": str(user.id), "username": user.username} for user in db_room.users]}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))