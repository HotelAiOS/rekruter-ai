import logging

logger = logging.getLogger(__name__)

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, JSON, Integer
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import uuid

class Company(Base):
    __tablename__ = "companies"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    jobs = relationship("Job", back_populates="company")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(JSON, nullable=False)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    company = relationship("Company", back_populates="jobs")
    candidates = relationship("Candidate", back_populates="job")

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String)
    parsed_cv = Column(JSON)
    score = Column(Integer, default=0)
    strengths = Column(JSON)
    weaknesses = Column(JSON)
    recommendation = Column(String)
    status = Column(String, default="new")
    created_at = Column(DateTime, default=datetime.utcnow)
    job = relationship("Job", back_populates="candidates")

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    company_id = Column(String, ForeignKey("companies.id"), nullable=False)
    role = Column(String, default="recruiter")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    company = relationship("Company")
