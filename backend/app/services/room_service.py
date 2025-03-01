from sqlalchemy.orm import Session
from app.models.room import Room
from app.utils.room_utils import generate_room_number
from uuid import UUID

def create_room(db: Session):
    # Generate a unique room number
    room_number = generate_room_number()
    while db.query(Room).filter(Room.room_number == room_number).first():
        room_number = generate_room_number()  # Ensure uniqueness

    # Create the room
    db_room = Room(room_number=room_number)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room
def join_room(db: Session, room_number: str, user_id: UUID):
    db_room = db.query(Room).filter(Room.room_number == room_number).first()
    if not db_room:
        raise ValueError("Room not found")

    # Add the user to the room if not already added
    if not db.query(RoomUser).filter(RoomUser.room_id == db_room.id, RoomUser.user_id == user_id).first():
        db_room_user = RoomUser(room_id=db_room.id, user_id=user_id)
        db.add(db_room_user)
        db.commit()
        db.refresh(db_room)

    return db_room