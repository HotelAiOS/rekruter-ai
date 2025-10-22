from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class Requirements(BaseModel):
    must_have: List[str]
    nice_to_have: List[str]

class JobCreate(BaseModel):
    title: str
    description: str
    requirements: Requirements

class JobResponse(BaseModel):
    id: UUID
    company_id: UUID
    title: str
    description: str
    requirements: dict
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[dict] = None
    status: Optional[str] = None

class JobStats(BaseModel):
    job_id: UUID
    total_candidates: int
    avg_score: float
    max_score: float
    min_score: float
    candidates_by_status: dict
    class Config:
        from_attributes = True

class CandidateResponse(BaseModel):
    id: UUID
    job_id: UUID
    name: str
    email: Optional[str]
    score: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

class CandidateUpdate(BaseModel):
    status: Optional[str] = None
    recommendation: Optional[str] = None
    class Config:
        from_attributes = True

class CandidateNote(BaseModel):
    text: str

class UserRegister(BaseModel):
    email: str
    password: str
    company_name: str

class UserResponse(BaseModel):
    id: UUID
    email: str
    company_id: UUID
    role: str
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
