# SecureBank Financial Services - Backend API

A FastAPI-based backend service for the three-tier financial/banking web application. This is the second tier (business logic layer) that provides REST API endpoints for managing financial plans and user enrollments.

## Features

- **RESTful API**: Clean REST endpoints following best practices
- **Data Validation**: Pydantic models for request/response validation
- **Business Logic**: Service layer for enrollment validation and processing
- **In-Memory Storage**: Mock data storage (ready for database integration)
- **CORS Support**: Configured for frontend integration
- **API Documentation**: Auto-generated Swagger/OpenAPI docs
- **Error Handling**: Comprehensive error handling and validation
- **Type Safety**: Full type hints throughout the codebase

## API Endpoints

### 1. GET /api/plans
Returns all available financial plans

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Savings Plan",
      "interest_rate": "3.5%",
      "term": "12 months",
      "min_contribution": 100,
      "max_contribution": 5000,
      "benefits": ["Flexible monthly contributions", "..."],
      "description": "Perfect for building your emergency fund..."
    }
  ],
  "total_plans": 4
}
```

### 2. POST /api/enroll
Creates a new user enrollment

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "address": "123 Main St, City, State",
  "selected_plan_id": 1,
  "monthly_contribution": 500.00
}
```

**Response:**
```json
{
  "success": true,
  "message": "Enrollment completed successfully",
  "enrollment_id": "uuid-string",
  "enrollment_data": {
    "enrollment_id": "uuid-string",
    "name": "John Doe",
    "email": "john@example.com",
    "selected_plan": {
      "id": 1,
      "name": "Savings Plan",
      "interest_rate": "3.5%",
      "term": "12 months"
    },
    "monthly_contribution": 500.00,
    "enrollment_date": "2025-08-07T18:00:00",
    "status": "active"
  }
}
```

### Additional Endpoints

- `GET /api/enroll/{enrollment_id}` - Get specific enrollment details
- `GET /api/enroll/` - Get all enrollments (admin/testing)
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

## Project Structure

```
financial-app-backend/
├── app/
│   ├── data/
│   │   ├── __init__.py
│   │   └── financial_plans.py     # Mock data for financial plans
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── plans.py               # Plans API endpoints
│   │   └── enrollment.py          # Enrollment API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── enrollment_service.py  # Business logic
│   └── __init__.py
├── main.py                        # FastAPI application
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

1. Navigate to the backend directory:
   ```bash
   cd financial-app-backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Access the API:
   - API Base URL: `http://localhost:8000`
   - Swagger Docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Alternative Running Methods

```bash
# Using the main.py file directly
python main.py

# Using uvicorn with specific settings
uvicorn main:app --reload --port 8000 --log-level info
```

## API Testing

### Using curl

**Get all plans:**
```bash
curl -X GET "http://localhost:8000/api/plans" \
     -H "accept: application/json"
```

**Create enrollment:**
```bash
curl -X POST "http://localhost:8000/api/enroll" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "phone": "1234567890",
       "address": "123 Main St, City, State",
       "selected_plan_id": 1,
       "monthly_contribution": 500.00
     }'
```

### Using Python requests

```python
import requests

# Get plans
response = requests.get("http://localhost:8000/api/plans")
print(response.json())

# Create enrollment
enrollment_data = {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "address": "123 Main St, City, State",
    "selected_plan_id": 1,
    "monthly_contribution": 500.00
}
response = requests.post("http://localhost:8000/api/enroll", json=enrollment_data)
print(response.json())
```

## Data Validation

The API includes comprehensive validation:

- **Required Fields**: Name, email, phone, address, plan ID, contribution
- **Email Format**: Valid email address format
- **Contribution Limits**: Within plan's min/max contribution range
- **Unique Email**: No duplicate enrollments for same email
- **Plan Validation**: Selected plan must exist

## Business Rules

1. **Contribution Validation**: Monthly contribution must be within the selected plan's limits
2. **Unique Enrollment**: One enrollment per email address
3. **Plan Existence**: Selected plan ID must be valid
4. **Data Integrity**: All required fields must be provided and valid

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful GET requests
- `201 Created` - Successful enrollment creation
- `400 Bad Request` - Validation errors
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server errors

Error responses follow this format:
```json
{
  "success": false,
  "message": "Error description",
  "details": "Additional error details"
}
```

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:3000` (React development server)
- `http://127.0.0.1:3000`

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation and settings management
- **python-multipart**: For handling form data
- **email-validator**: Email validation support

## Development Notes

- All data is currently stored in-memory using Python dictionaries
- No database integration yet (ready for future implementation)
- UUID-based enrollment IDs for uniqueness
- Full type hints for better IDE support and code quality
- Modular structure for easy maintenance and testing

## Future Enhancements

When integrating with a database:

1. Replace in-memory storage with database models
2. Add database connection and session management
3. Implement proper data persistence
4. Add database migrations
5. Enhance error handling for database operations

## Testing

The API can be tested using:
- Swagger UI at `/docs`
- ReDoc at `/redoc`
- curl commands
- Python requests library
- Postman or similar API testing tools

## Production Considerations

For production deployment:
- Add authentication and authorization
- Implement rate limiting
- Add logging and monitoring
- Use environment variables for configuration
- Add database connection pooling
- Implement proper error logging
