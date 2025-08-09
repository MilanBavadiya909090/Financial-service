from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.database_models import FinancialPlan, PlanBenefit, Enrollment
from app.models.schemas import PlansResponse, EnrollmentRequest
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service layer for database operations"""
    
    @staticmethod
    def get_all_financial_plans(db: Session) -> List[dict]:
        """Get all active financial plans from database"""
        try:
            plans = db.query(FinancialPlan).filter(FinancialPlan.is_active == True).all()
            
            result = []
            for plan in plans:
                # Get benefits for this plan
                benefits = [benefit.benefit_text for benefit in plan.benefits]
                
                plan_dict = {
                    "id": plan.id,
                    "name": plan.name,
                    "interest_rate": plan.interest_rate,
                    "term": plan.term,
                    "min_contribution": plan.min_contribution,
                    "max_contribution": plan.max_contribution,
                    "benefits": benefits,
                    "description": plan.description
                }
                result.append(plan_dict)
            
            logger.info(f"Retrieved {len(result)} financial plans from database")
            return result
            
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving financial plans: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving financial plans: {str(e)}")
            raise
    
    @staticmethod
    def create_enrollment(db: Session, enrollment_data: EnrollmentRequest) -> dict:
        """Create a new enrollment in database"""
        try:
            # Use the correct field name from the schema
            plan_id = enrollment_data.selected_plan_id
            
            # Check if plan exists
            plan = db.query(FinancialPlan).filter(
                FinancialPlan.id == plan_id,
                FinancialPlan.is_active == True
            ).first()
            
            if not plan:
                raise ValueError(f"Plan with ID {plan_id} not found or inactive")
            
            # Validate contribution amount
            if (enrollment_data.monthly_contribution < plan.min_contribution or 
                enrollment_data.monthly_contribution > plan.max_contribution):
                raise ValueError(
                    f"Monthly contribution must be between ${plan.min_contribution} and ${plan.max_contribution}"
                )
            
            # Create enrollment
            enrollment = Enrollment(
                plan_id=plan_id,
                full_name=enrollment_data.name,
                email=enrollment_data.email,
                phone=enrollment_data.phone,
                monthly_contribution=int(enrollment_data.monthly_contribution),
                status="pending"
            )
            
            db.add(enrollment)
            db.commit()
            db.refresh(enrollment)
            
            logger.info(f"Created enrollment for {enrollment_data.email} in plan {plan_id}")
            
            return {
                "id": enrollment.id,
                "plan_id": enrollment.plan_id,
                "plan_name": plan.name,
                "full_name": enrollment.full_name,
                "email": enrollment.email,
                "phone": enrollment.phone,
                "monthly_contribution": enrollment.monthly_contribution,
                "status": enrollment.status,
                "enrollment_date": enrollment.enrollment_date.isoformat()
            }
            
        except ValueError as e:
            logger.warning(f"Validation error creating enrollment: {str(e)}")
            raise
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error creating enrollment: {str(e)}")
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating enrollment: {str(e)}")
            raise
    
    @staticmethod
    def get_enrollment_by_id(db: Session, enrollment_id: int) -> Optional[dict]:
        """Get enrollment by ID"""
        try:
            enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
            
            if not enrollment:
                return None
            
            return {
                "id": enrollment.id,
                "plan_id": enrollment.plan_id,
                "plan_name": enrollment.plan.name,
                "full_name": enrollment.full_name,
                "email": enrollment.email,
                "phone": enrollment.phone,
                "monthly_contribution": enrollment.monthly_contribution,
                "status": enrollment.status,
                "enrollment_date": enrollment.enrollment_date.isoformat()
            }
            
        except SQLAlchemyError as e:
            logger.error(f"Database error retrieving enrollment {enrollment_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error retrieving enrollment {enrollment_id}: {str(e)}")
            raise
    
    @staticmethod
    def seed_initial_data(db: Session):
        """Seed initial financial plans data"""
        try:
            # Check if data already exists
            existing_plans = db.query(FinancialPlan).count()
            if existing_plans > 0:
                logger.info("Financial plans already exist, skipping seed data")
                return
            
            # Initial financial plans data
            plans_data = [
                {
                    "name": "Savings Plan",
                    "interest_rate": "3.5%",
                    "term": "12 months",
                    "min_contribution": 100,
                    "max_contribution": 5000,
                    "description": "Perfect for building your emergency fund with competitive interest rates and complete flexibility.",
                    "benefits": [
                        "Flexible monthly contributions",
                        "No lock-in period",
                        "Instant withdrawals",
                        "Mobile banking access"
                    ]
                },
                {
                    "name": "Premium Plan",
                    "interest_rate": "5.2%",
                    "term": "24 months",
                    "min_contribution": 500,
                    "max_contribution": 10000,
                    "description": "Enhanced savings plan with premium benefits and higher returns for serious savers.",
                    "benefits": [
                        "Higher interest rates",
                        "Priority customer support",
                        "Quarterly bonus rewards",
                        "Free financial consultation"
                    ]
                },
                {
                    "name": "Retirement Plan",
                    "interest_rate": "6.8%",
                    "term": "60 months",
                    "min_contribution": 200,
                    "max_contribution": 15000,
                    "description": "Long-term investment plan designed to secure your financial future with maximum growth potential.",
                    "benefits": [
                        "Tax advantages",
                        "Compound interest growth",
                        "Retirement planning tools",
                        "Estate planning support"
                    ]
                },
                {
                    "name": "Education Plan",
                    "interest_rate": "4.7%",
                    "term": "36 months",
                    "min_contribution": 150,
                    "max_contribution": 8000,
                    "description": "Specially designed to help you save for educational expenses with steady growth and flexibility.",
                    "benefits": [
                        "Education-focused savings",
                        "Flexible contribution schedule",
                        "Goal tracking tools",
                        "Educational resources"
                    ]
                }
            ]
            
            # Create plans and benefits
            for plan_data in plans_data:
                benefits = plan_data.pop("benefits")
                
                # Create plan
                plan = FinancialPlan(**plan_data)
                db.add(plan)
                db.flush()  # Get the ID
                
                # Create benefits
                for benefit_text in benefits:
                    benefit = PlanBenefit(plan_id=plan.id, benefit_text=benefit_text)
                    db.add(benefit)
            
            db.commit()
            logger.info("Successfully seeded initial financial plans data")
            
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error seeding initial data: {str(e)}")
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error seeding initial data: {str(e)}")
            raise
