from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class CodeFileCreate(BaseModel):
    filename: str
    content: str
    room_number: str

class CodeFileUpdate(BaseModel):
    content: str

class CodeFileResponse(BaseModel):
    id: UUID
    filename: str
    user_id: UUID
    content: str

class CodeFileUpdateResponse(BaseModel):
    id: UUID
    filename: str
    user_id: UUID

class CodeHistoryResponse(BaseModel):
    id: int
    content: str
    updated_at: datetime

class CodeAnalysisRequest(BaseModel):
    code: str  # The code to analyze

class CodeAnalysisResponse(BaseModel):
    analysis: str  # The analysis result