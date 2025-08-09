import uuid
from datetime import datetime
from typing import Dict, List
from app.models.schemas import EnrollmentRequest, EnrollmentResponse, FinancialPlan
from app.data.financial_plans import get_plan_by_id

# In-memory storage for enrollments (will be replaced with database later)
enrollments_storage: Dict[str, dict] = {}

class EnrollmentService:
    
    @staticmethod
    def validate_enrollment(enrollment_data: EnrollmentRequest) -> tuple[bool, str]:
        """Validate enrollment data against business rules"""
        
        # Get the selected plan
        selected_plan = get_plan_by_id(enrollment_data.selected_plan_id)
        if not selected_plan:
            return False, f"Invalid plan ID: {enrollment_data.selected_plan_id}"
        
        # Validate contribution amount
        if enrollment_data.monthly_contribution < selected_plan.min_contribution:
            return False, f"Monthly contribution must be at least ${selected_plan.min_contribution}"
        
        if enrollment_data.monthly_contribution > selected_plan.max_contribution:
            return False, f"Monthly contribution cannot exceed ${selected_plan.max_contribution}"
        
        # REMOVED: Email uniqueness check - now allowing duplicate emails
        # This allows the same person to enroll in multiple plans or 
        # create multiple enrollments as needed
        
        return True, "Validation successful"
    
    @staticmethod
    def create_enrollment(enrollment_data: EnrollmentRequest) -> EnrollmentResponse:
        """Create a new enrollment"""
        
        # Validate the enrollment
        is_valid, validation_message = EnrollmentService.validate_enrollment(enrollment_data)
        if not is_valid:
            return EnrollmentResponse(
                success=False,
                message=validation_message,
                enrollment_id=""
            )
        
        # Generate unique enrollment ID
        enrollment_id = str(uuid.uuid4())
        
        # Get the selected plan details
        selected_plan = get_plan_by_id(enrollment_data.selected_plan_id)
        
        # Create enrollment record
        enrollment_record = {
            "enrollment_id": enrollment_id,
            "name": enrollment_data.name,
            "email": enrollment_data.email,
            "phone": enrollment_data.phone,
            "address": enrollment_data.address,
            "selected_plan": {
                "id": selected_plan.id,
                "name": selected_plan.name,
                "interest_rate": selected_plan.interest_rate,
                "term": selected_plan.term
            },
            "monthly_contribution": enrollment_data.monthly_contribution,
            "enrollment_date": datetime.now().isoformat(),
            "status": "active"
        }
        
        # Store in memory (will be database later)
        enrollments_storage[enrollment_id] = enrollment_record
        
        return EnrollmentResponse(
            success=True,
            message="Enrollment completed successfully",
            enrollment_id=enrollment_id,
            enrollment_data=enrollment_record
        )
    
    @staticmethod
    def get_enrollment(enrollment_id: str) -> dict:
        """Get enrollment by ID"""
        return enrollments_storage.get(enrollment_id)
    
    @staticmethod
    def get_all_enrollments() -> List[dict]:
        """Get all enrollments (for admin purposes)"""
        return list(enrollments_storage.values())
    
    @staticmethod
    def get_enrollments_count() -> int:
        """Get total number of enrollments"""
        return len(enrollments_storage)
    
    @staticmethod
    def get_enrollments_by_email(email: str) -> List[dict]:
        """Get all enrollments for a specific email address"""
        return [enrollment for enrollment in enrollments_storage.values() 
                if enrollment.get('email') == email]
    
    @staticmethod
    def get_enrollment_statistics() -> dict:
        """Get enrollment statistics"""
        enrollments = list(enrollments_storage.values())
        
        # Count enrollments by plan
        plan_counts = {}
        email_counts = {}
        
        for enrollment in enrollments:
            plan_name = enrollment['selected_plan']['name']
            email = enrollment['email']
            
            plan_counts[plan_name] = plan_counts.get(plan_name, 0) + 1
            email_counts[email] = email_counts.get(email, 0) + 1
        
        # Find emails with multiple enrollments
        duplicate_emails = {email: count for email, count in email_counts.items() if count > 1}
        
        return {
            "total_enrollments": len(enrollments),
            "unique_emails": len(email_counts),
            "duplicate_emails": len(duplicate_emails),
            "enrollments_by_plan": plan_counts,
            "emails_with_multiple_enrollments": duplicate_emails
        }
