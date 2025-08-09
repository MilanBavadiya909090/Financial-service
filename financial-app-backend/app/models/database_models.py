from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class FinancialPlan(Base):
    """Financial Plan model"""
    __tablename__ = "financial_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    interest_rate = Column(String(10), nullable=False)
    term = Column(String(50), nullable=False)
    min_contribution = Column(Integer, nullable=False)
    max_contribution = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationship with benefits
    benefits = relationship("PlanBenefit", back_populates="plan", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="plan")

class PlanBenefit(Base):
    """Plan Benefits model"""
    __tablename__ = "plan_benefits"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("financial_plans.id"), nullable=False)
    benefit_text = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    plan = relationship("FinancialPlan", back_populates="benefits")

class Enrollment(Base):
    """User Enrollment model"""
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("financial_plans.id"), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    monthly_contribution = Column(Integer, nullable=False)
    enrollment_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="pending")  # pending, approved, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    plan = relationship("FinancialPlan", back_populates="enrollments")

class User(Base):
    """User model for future authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
