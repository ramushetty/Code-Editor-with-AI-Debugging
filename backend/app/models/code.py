from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import uuid

class CodeFile(Base):
    __tablename__ = "code_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  
    filename = Column(String, index=True)
    file_path = Column(String)  # Path to the file in the file system
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))  
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id"))  # Associate with a room
    owner = relationship("User", back_populates="code_files")
    room = relationship("Room", back_populates="code_files")
    history = relationship("CodeHistory", back_populates="code_file")

class CodeHistory(Base):
    __tablename__ = "code_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    code_file_id = Column(UUID(as_uuid=True), ForeignKey("code_files.id"))
    content = Column(Text)  # Store the previous code content
    updated_at = Column(DateTime, default=datetime.utcnow)
    code_file = relationship("CodeFile", back_populates="history")