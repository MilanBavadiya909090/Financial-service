from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class FinancialPlan(BaseModel):
    id: int
    name: str
    interest_rate: str
    term: str
    min_contribution: int
    max_contribution: int
    benefits: List[str]
    description: str

class EnrollmentRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of the applicant")
    email: EmailStr = Field(..., description="Valid email address")
    phone: str = Field(..., min_length=10, max_length=15, description="Phone number")
    address: str = Field(..., min_length=10, max_length=200, description="Full address")
    selected_plan_id: int = Field(..., description="ID of the selected financial plan")
    monthly_contribution: float = Field(..., gt=0, description="Monthly contribution amount")

class EnrollmentResponse(BaseModel):
    success: bool
    message: str
    enrollment_id: str
    enrollment_data: Optional[dict] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    details: Optional[dict] = None

class PlansResponse(BaseModel):
    success: bool = True
    data: List[FinancialPlan]
    total_plans: int
