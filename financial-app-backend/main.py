from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import plans, enrollment
from app.database import init_database, create_tables, check_database_health
from app.services.database_service import DatabaseService
from app.database import get_database_session
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="SecureBank Financial Services API",
    description="Backend API for financial/banking web application",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for ECS deployment
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Database initialization
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        logger.info("Initializing database connection...")
        init_database()
        
        logger.info("Creating database tables...")
        create_tables()
        
        # Seed initial data
        logger.info("Seeding initial data...")
        db = next(get_database_session())
        try:
            DatabaseService.seed_initial_data(db)
        finally:
            db.close()
        
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        # Don't fail startup - allow app to run with fallback data
        logger.warning("Application will continue with fallback data")

# Include routers
app.include_router(plans.router, prefix="/api")
app.include_router(enrollment.router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "SecureBank Financial Services API",
        "version": "1.0.0",
        "status": "active",
        "database_connected": check_database_health(),
        "endpoints": {
            "plans": "/api/plans",
            "enrollment": "/api/enroll",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_healthy = check_database_health()
    
    return {
        "status": "healthy" if db_healthy else "degraded",
        "service": "SecureBank Financial API",
        "database": "connected" if db_healthy else "disconnected",
        "timestamp": "2025-08-07T18:00:00Z"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "details": str(exc) if app.debug else "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
