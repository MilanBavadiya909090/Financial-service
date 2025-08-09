from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.models.schemas import EnrollmentRequest, EnrollmentResponse, ErrorResponse
from app.database import get_database_session
from app.services.database_service import DatabaseService
from app.services.enrollment_service import EnrollmentService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/enroll", tags=["Enrollment"])

@router.post("/", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def create_enrollment(
    enrollment_data: EnrollmentRequest,
    db: Session = Depends(get_database_session)
):
    """
    Create a new enrollment for a financial plan
    
    Args:
        enrollment_data (EnrollmentRequest): User enrollment information
        db: Database session
        
    Returns:
        EnrollmentResponse: Success status and enrollment details
        
    Raises:
        HTTPException: If validation fails or enrollment cannot be created
    """
    try:
        # Try database first
        try:
            enrollment = DatabaseService.create_enrollment(db, enrollment_data)
            
            return EnrollmentResponse(
                success=True,
                message="Enrollment submitted successfully! You will receive a confirmation email shortly.",
                enrollment_id=str(enrollment["id"]),  # Convert to string
                enrollment_data={
                    "enrollment_id": str(enrollment["id"]),
                    "name": enrollment["full_name"],
                    "email": enrollment["email"],
                    "phone": enrollment["phone"],
                    "selected_plan": {
                        "id": enrollment["plan_id"],
                        "name": enrollment["plan_name"]
                    },
                    "monthly_contribution": float(enrollment["monthly_contribution"]),
                    "enrollment_date": enrollment["enrollment_date"],
                    "status": enrollment["status"]
                }
            )
            
        except Exception as db_error:
            logger.warning(f"Database error, falling back to service: {str(db_error)}")
            # Fallback to original service
            result = EnrollmentService.create_enrollment(enrollment_data)
            
            if not result.success:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result.message
                )
            
            return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating enrollment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/{enrollment_id}")
async def get_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_database_session)
):
    """
    Get enrollment details by ID
    
    Args:
        enrollment_id (int): Unique enrollment identifier
        db: Database session
        
    Returns:
        dict: Enrollment details
    """
    try:
        # Try database first
        try:
            enrollment = DatabaseService.get_enrollment_by_id(db, enrollment_id)
            
            if not enrollment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Enrollment not found with ID: {enrollment_id}"
                )
            
            return {
                "success": True,
                "data": enrollment
            }
            
        except HTTPException:
            raise
        except Exception as db_error:
            logger.warning(f"Database error, falling back to service: {str(db_error)}")
            # Fallback to original service
            enrollment = EnrollmentService.get_enrollment(str(enrollment_id))
            
            if not enrollment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Enrollment not found with ID: {enrollment_id}"
                )
            
            return {
                "success": True,
                "data": enrollment
            }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving enrollment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/")
async def get_all_enrollments():
    """
    Get all enrollments (for admin/testing purposes)
    
    Returns:
        dict: List of all enrollments with statistics
    """
    try:
        enrollments = EnrollmentService.get_all_enrollments()
        stats = EnrollmentService.get_enrollment_statistics()
        
        return {
            "success": True,
            "data": enrollments,
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/by-email/{email}")
async def get_enrollments_by_email(email: str):
    """
    Get all enrollments for a specific email address
    
    Args:
        email (str): Email address to search for
        
    Returns:
        dict: List of enrollments for the specified email
    """
    try:
        enrollments = EnrollmentService.get_enrollments_by_email(email)
        
        return {
            "success": True,
            "email": email,
            "enrollment_count": len(enrollments),
            "enrollments": enrollments
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/statistics/summary")
async def get_enrollment_statistics():
    """
    Get enrollment statistics including duplicate email information
    
    Returns:
        dict: Comprehensive enrollment statistics
    """
    try:
        stats = EnrollmentService.get_enrollment_statistics()
        
        return {
            "success": True,
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
