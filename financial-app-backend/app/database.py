import json
import boto3
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database base class
Base = declarative_base()

# Global variables
engine = None
SessionLocal = None

def get_database_credentials():
    """Retrieve database credentials from AWS Secrets Manager"""
    try:
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name='us-east-1'
        )
        
        # Retrieve the secret - use environment-aware secret name
        import os
        environment = os.getenv("ENVIRONMENT", "dev")
        secret_name = f"financial-app-{environment}/database"
        response = client.get_secret_value(SecretId=secret_name)
        
        # Parse the secret
        secret = json.loads(response['SecretString'])
        return secret
    
    except Exception as e:
        logger.error(f"Error retrieving database credentials: {str(e)}")
        # Fallback to environment variables for local development
        import os
        return {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", 3306)),
            "username": os.getenv("DB_USER", "admin"),  # Changed from DB_USERNAME to DB_USER
            "password": os.getenv("DB_PASSWORD", ""),
            "dbname": os.getenv("DB_NAME", "financial_app")
        }

def create_database_if_not_exists():
    """Create the database if it doesn't exist"""
    try:
        # Get database credentials
        db_config = get_database_credentials()
        
        # Create connection string without database name
        connection_string = (
            f"mysql+pymysql://{db_config['username']}:{db_config['password']}"
            f"@{db_config['host']}:{db_config['port']}"
            f"?charset=utf8mb4"
        )
        
        # Create temporary engine to create database
        temp_engine = create_engine(connection_string)
        
        with temp_engine.connect() as connection:
            # Create database if it doesn't exist
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_config['dbname']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            connection.commit()
            logger.info(f"Database '{db_config['dbname']}' created or already exists")
        
        temp_engine.dispose()
        
    except Exception as e:
        logger.error(f"Error creating database: {str(e)}")
        raise

def create_database_engine():
    """Create database engine with connection pooling"""
    global engine
    
    try:
        # First, ensure database exists
        create_database_if_not_exists()
        
        # Get database credentials
        db_config = get_database_credentials()
        
        # Create connection string
        connection_string = (
            f"mysql+pymysql://{db_config['username']}:{db_config['password']}"
            f"@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
            f"?charset=utf8mb4"
        )
        
        # Create engine with connection pooling
        engine = create_engine(
            connection_string,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False  # Set to True for SQL debugging
        )
        
        logger.info("Database engine created successfully")
        return engine
        
    except Exception as e:
        logger.error(f"Error creating database engine: {str(e)}")
        raise

def create_session_factory():
    """Create session factory"""
    global SessionLocal, engine
    
    if engine is None:
        engine = create_database_engine()
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database session factory created successfully")

def get_database_session():
    """Get database session"""
    if SessionLocal is None:
        create_session_factory()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database connection"""
    try:
        create_session_factory()
        
        # Test the connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

def create_tables():
    """Create database tables"""
    try:
        if engine is None:
            create_database_engine()
            
        # Import all models to ensure they're registered
        from app.models import database_models
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

# Health check function
def check_database_health():
    """Check database connectivity for health checks"""
    try:
        if engine is None:
            return False
            
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return True
            
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return False
