from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.code import CodeAnalysisRequest, CodeAnalysisResponse
from app.services.ai_service import analyze_code
from app.core.database import get_db
from app.core.security import get_current_user
from uuid import UUID

router = APIRouter()

@router.post("/analyze", response_model=CodeAnalysisResponse)
def analyze_code_endpoint(request: CodeAnalysisRequest, db: Session = Depends(get_db), current_user: UUID = Depends(get_current_user)):
    try:
        # Analyze the code using the AI service
        analysis = analyze_code(request.code)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))