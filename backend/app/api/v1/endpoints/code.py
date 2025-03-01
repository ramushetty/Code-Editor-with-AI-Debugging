from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.code import CodeFileCreate, CodeFileUpdate, CodeFileResponse, CodeHistoryResponse, CodeFileUpdateResponse
from app.services.code_service import create_code_file, update_code_file, get_code_file, delete_code_file, get_code_history
from app.core.database import get_db
from app.core.security import get_current_user
from uuid import UUID

router = APIRouter()

@router.post("/code_files", response_model=CodeFileResponse)
def create_code_file_endpoint(code_file: CodeFileCreate, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    try:
        return create_code_file(db, code_file, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/code_files/{code_file_id}", response_model=CodeFileUpdateResponse)
def update_code_file_endpoint(code_file_id: UUID, code_file: CodeFileUpdate, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    try:
        return update_code_file(db, code_file_id, code_file.content, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/code_files/{code_file_id}", response_model=CodeFileResponse)
def get_code_file_endpoint(code_file_id: UUID, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    try:
        return get_code_file(db, code_file_id, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/code_files/{code_file_id}")
def delete_code_file_endpoint(code_file_id: UUID, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    try:
        delete_code_file(db, code_file_id, current_user_id)
        return {"message": "Code file deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/code_files/{code_file_id}/history", response_model=list[CodeHistoryResponse])
def get_code_history_endpoint(code_file_id: UUID, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    try:
        return get_code_history(db, code_file_id, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))