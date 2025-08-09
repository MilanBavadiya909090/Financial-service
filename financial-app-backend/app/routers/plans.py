from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.schemas import PlansResponse, ErrorResponse
from app.data.financial_plans import get_all_plans
from app.database import get_database_session
from app.services.database_service import DatabaseService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/plans", tags=["Financial Plans"])

@router.get("/", response_model=PlansResponse)
async def get_financial_plans(db: Session = Depends(get_database_session)):
    """
    Get all available financial plans
    
    Returns:
        PlansResponse: List of all financial plans with their details
    """
    try:
        # Try to get plans from database first
        try:
            plans = DatabaseService.get_all_financial_plans(db)
            logger.info(f"Retrieved {len(plans)} plans from database")
        except Exception as db_error:
            logger.warning(f"Database error, falling back to static data: {str(db_error)}")
            # Fallback to static data if database is unavailable
            plans = get_all_plans()
        
        return PlansResponse(
            success=True,
            data=plans,
            total_plans=len(plans)
        )
    except Exception as e:
        logger.error(f"Error retrieving financial plans: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
