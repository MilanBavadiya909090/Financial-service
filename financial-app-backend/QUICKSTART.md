# Quick Start Guide - SecureBank Financial Services Backend

## 🚀 Getting Started

### 1. Install Dependencies
```bash
cd financial-app-backend
pip install fastapi uvicorn[standard] python-multipart email-validator
```

### 2. Verify Setup
```bash
python verify_setup.py
```

### 3. Start the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test the API
- **API Base URL**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Quick API Tests

### Get Financial Plans
```bash
curl -X GET "http://localhost:8000/api/plans"
```

### Create Enrollment
```bash
curl -X POST "http://localhost:8000/api/enroll" \
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

### Run Test Script
```bash
python test_api.py
```

## 📁 Project Structure
```
financial-app-backend/
├── main.py                    # FastAPI application entry point
├── app/
│   ├── data/
│   │   └── financial_plans.py # Mock financial plans data
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── routers/
│   │   ├── plans.py           # GET /api/plans endpoint
│   │   └── enrollment.py      # POST /api/enroll endpoint
│   └── services/
│       └── enrollment_service.py # Business logic
├── requirements.txt           # Python dependencies
├── README.md                 # Detailed documentation
├── QUICKSTART.md            # This file
├── verify_setup.py          # Setup verification script
└── test_api.py              # API testing script
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/plans` | Get all financial plans |
| POST | `/api/enroll` | Create new enrollment |
| GET | `/api/enroll/{id}` | Get enrollment by ID |
| GET | `/api/enroll/` | Get all enrollments |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger UI |

## 🎯 Next Steps

1. **Start the backend server** using the command above
2. **Test the API** using the provided curl commands or Swagger UI
3. **Integrate with frontend** by updating the React app to make HTTP calls
4. **Add database integration** when ready for the third tier

## 🔧 Development Notes

- All data is currently stored in-memory
- CORS is configured for `http://localhost:3000` (React dev server)
- Full input validation with Pydantic models
- Comprehensive error handling
- Auto-generated API documentation
