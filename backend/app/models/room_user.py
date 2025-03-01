from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid

class RoomUser(Base):
    __tablename__ = "room_users"

    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)