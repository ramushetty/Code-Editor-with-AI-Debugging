from sqlalchemy.orm import Session
from app.models.code import CodeFile, CodeHistory
from app.models.room import Room
from app.schemas.code import CodeFileCreate
from app.utils.file_utils import save_code_file, read_code_file, delete_code_file
from app.core.redis import redis_client
from datetime import datetime
from uuid import UUID
import json

def create_code_file(db: Session, code_file: CodeFileCreate, user_id: UUID):
    # Save the file to the file system
    file_path = save_code_file(code_file.filename, code_file.content, user_id)
    room_id = db.query(Room).filter(Room.room_number == code_file.room_number).first()
    # Save metadata to the database
    db_code_file = CodeFile(
        filename=code_file.filename,
        file_path=str(file_path),
        user_id=user_id,
        room_id=str(room_id.id)  # Associate with the room
    )
    db.add(db_code_file)
    db.commit()
    db.refresh(db_code_file)

    # Cache the new code file
    cache_key = f"code_file:{db_code_file.id}"
    result = {"id": str(db_code_file.id), "filename": db_code_file.filename, "content": code_file.content, "user_id": str(user_id)}
    redis_client.set(cache_key, json.dumps(result), ex=3600)  # Cache for 1 hour

    return db_code_file

def update_code_file(db: Session, code_file_id: int, content: str, user_id: UUID):
    db_code_file = db.query(CodeFile).filter(CodeFile.id == code_file_id).first()
    if not db_code_file:
        raise ValueError("Code file not found")

    # Save the current content to history
    current_content = read_code_file(db_code_file.filename, db_code_file.user_id)
    db_history = CodeHistory(code_file_id=code_file_id, content=current_content, updated_at=datetime.utcnow())
    db.add(db_history)

    # Update the file content
    save_code_file(db_code_file.filename, content, db_code_file.user_id)
    db.commit()
    db.refresh(db_code_file)

    # Update the cache
    cache_key = f"code_file:{code_file_id}"
    result = {"id": str(db_code_file.id), "filename": db_code_file.filename, "content": content, "user_id": str(user_id)}
    redis_client.set(cache_key, json.dumps(result), ex=3600)  # Cache for 1 hour

    return db_code_file

def get_code_file(db: Session, code_file_id: int, user_id: UUID):
    cache_key = f"code_file:{code_file_id}"
    cached_data = redis_client.get(cache_key)
    print(cached_data)
    if cached_data:
        return json.loads(cached_data)

    db_code_file = db.query(CodeFile).filter(CodeFile.id == code_file_id, CodeFile.user_id == user_id).first()
    if not db_code_file:
        raise ValueError("Code file not found")

    content = read_code_file(db_code_file.filename, user_id)
    result = {"id": str(db_code_file.id), "filename": db_code_file.filename, "content": content, "user_id": str(user_id)}
    redis_client.set(cache_key, json.dumps(result), ex=3600)  # Cache for 1 hour
    return result

def delete_code_file(db: Session, code_file_id: int, user_id: UUID):
    db_code_file = db.query(CodeFile).filter(CodeFile.id == code_file_id, CodeFile.user_id == user_id).first()
    if not db_code_file:
        raise ValueError("Code file not found")

    # Delete the file from the file system
    delete_code_file(db_code_file.filename, user_id)

    # Delete the cache
    cache_key = f"code_file:{code_file_id}"
    redis_client.delete(cache_key)

    # Delete the database record
    db.delete(db_code_file)
    db.commit()

def get_code_history(db: Session, code_file_id: int, user_id: UUID):
    db_code_file = db.query(CodeFile).filter(CodeFile.id == code_file_id, CodeFile.user_id == user_id).first()
    if not db_code_file:
        raise ValueError("Code file not found")
    return db_code_file.history