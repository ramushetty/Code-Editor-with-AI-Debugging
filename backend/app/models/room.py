from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Room(Base):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    room_number = Column(String, unique=True, index=True)  # Unique 6-character room number
    users = relationship("User", secondary="room_users", back_populates="rooms")
    code_files = relationship("CodeFile", back_populates="room") 