from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID
from database import get_db
from models import Job, Candidate
from schemas import CandidateResponse, CandidateUpdate, CandidateNote
from services.pdf_parser import PDFParserService
from services.llm_service import LLMService
from services.agents.orchestrator import MultiAgentOrchestrator
from config import settings
import logging

router = APIRouter(prefix="/api", tags=["candidates"])
logger = logging.getLogger(__name__)

pdf_parser = PDFParserService()
llm_service = LLMService()

@router.post("/jobs/{job_id}/upload", status_code=status.HTTP_201_CREATED)
async def upload_cv(
    job_id: UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Upload CV for job application"""
    # Check if job exists
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Validate file type
    allowed_types = ["application/pdf", "text/plain", "application/msword"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=422, detail="Invalid file type")
    
    try:
        # Save file temporarily
        import tempfile
        from pathlib import Path
        
        temp_file = Path(tempfile.mktemp(suffix=Path(file.filename).suffix))
        content = await file.read()
        temp_file.write_bytes(content)
        
        # Parse CV
        cv_text = pdf_parser.extract_text(str(temp_file))
        temp_file.unlink()
        
        # Parse CV with LLM
        parsed_cv = await llm_service.parse_cv(cv_text)
        
        # Score candidate
        if settings.USE_MULTI_AGENT:
            orchestrator = MultiAgentOrchestrator()
            scoring_result = await orchestrator.process_candidate(
                cv_data=parsed_cv,
                job_requirements=job.requirements
            )
        else:
            scoring_result = await llm_service.score_candidate(
                parsed_cv, 
                job.requirements
            )
        
        # Create candidate
        candidate = Candidate(
            job_id=job_id,
            name=parsed_cv.get("name", "Unknown"),
            email=parsed_cv.get("email", ""),
            parsed_cv=parsed_cv,
            score=scoring_result.get("score", 0),
            strengths=scoring_result.get("strengths", []),
            weaknesses=scoring_result.get("weaknesses", []),
            recommendation=scoring_result.get("recommendation", "pending"),
            status="new"
        )
        
        db.add(candidate)
        await db.commit()
        await db.refresh(candidate)
        
        return {
            "candidate_id": candidate.id,
            "score": candidate.score,
            "recommendation": candidate.recommendation
        }
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error processing CV: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs/{job_id}/candidates", response_model=List[CandidateResponse])
async def list_candidates(
    job_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    min_score: Optional[int] = Query(None, ge=0, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List candidates for specific job"""
    query = select(Candidate).where(Candidate.job_id == job_id)
    
    if status_filter:
        query = query.where(Candidate.status == status_filter)
    
    if min_score is not None:
        query = query.where(Candidate.score >= min_score)
    
    query = query.offset(skip).limit(limit).order_by(Candidate.score.desc())
    
    result = await db.execute(query)
    candidates = result.scalars().all()
    
    return candidates

@router.get("/candidates/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get single candidate details"""
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    return candidate

@router.put("/candidates/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: UUID,
    candidate_data: CandidateUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update candidate status/notes"""
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    update_data = candidate_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(candidate, field, value)
    
    await db.commit()
    await db.refresh(candidate)
    
    return candidate

@router.delete("/candidates/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    candidate_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete candidate"""
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    await db.delete(candidate)
    await db.commit()
    
    return None

@router.post("/candidates/{candidate_id}/notes", status_code=status.HTTP_201_CREATED)
async def add_candidate_note(
    candidate_id: UUID,
    note_data: CandidateNote,
    db: AsyncSession = Depends(get_db)
):
    """Add recruiter note to candidate"""
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Add note to candidate metadata
    if not candidate.parsed_cv:
        candidate.parsed_cv = {}
    
    if "notes" not in candidate.parsed_cv:
        candidate.parsed_cv["notes"] = []
    
    from datetime import datetime
    candidate.parsed_cv["notes"].append({
        "text": note_data.text,
        "created_at": datetime.utcnow().isoformat(),
        "author": "recruiter"  # Will be replaced with actual user
    })
    
    await db.commit()
    
    return {"message": "Note added successfully"}
