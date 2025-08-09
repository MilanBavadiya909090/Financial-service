from app.models.schemas import FinancialPlan

# Mock data for financial plans
FINANCIAL_PLANS = [
    FinancialPlan(
        id=1,
        name="Savings Plan",
        interest_rate="3.5%",
        term="12 months",
        min_contribution=100,
        max_contribution=5000,
        benefits=[
            "Flexible monthly contributions",
            "No lock-in period",
            "Instant withdrawals",
            "Mobile banking access"
        ],
        description="Perfect for building your emergency fund with competitive interest rates and complete flexibility."
    ),
    FinancialPlan(
        id=2,
        name="Premium Plan",
        interest_rate="5.2%",
        term="24 months",
        min_contribution=500,
        max_contribution=10000,
        benefits=[
            "Higher interest rates",
            "Priority customer support",
            "Quarterly bonus rewards",
            "Free financial consultation"
        ],
        description="Enhanced savings plan with premium benefits and higher returns for serious savers."
    ),
    FinancialPlan(
        id=3,
        name="Retirement Plan",
        interest_rate="6.8%",
        term="60 months",
        min_contribution=200,
        max_contribution=15000,
        benefits=[
            "Tax advantages",
            "Compound interest growth",
            "Retirement planning tools",
            "Estate planning support"
        ],
        description="Long-term investment plan designed to secure your financial future with maximum growth potential."
    ),
    FinancialPlan(
        id=4,
        name="Education Plan",
        interest_rate="4.7%",
        term="36 months",
        min_contribution=150,
        max_contribution=8000,
        benefits=[
            "Education-focused savings",
            "Flexible contribution schedule",
            "Goal tracking tools",
            "Educational resources"
        ],
        description="Specially designed to help you save for educational expenses with steady growth and flexibility."
    )
]

def get_all_plans():
    """Return all available financial plans"""
    return FINANCIAL_PLANS

def get_plan_by_id(plan_id: int):
    """Get a specific plan by ID"""
    for plan in FINANCIAL_PLANS:
        if plan.id == plan_id:
            return plan
    return None
