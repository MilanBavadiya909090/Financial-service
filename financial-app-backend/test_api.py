#!/usr/bin/env python3
"""
Simple test script to verify the Financial Services API functionality
Run this after starting the server with: uvicorn main:app --reload
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    print()

def test_get_plans():
    """Test getting all financial plans"""
    print("🔍 Testing GET /api/plans...")
    try:
        response = requests.get(f"{BASE_URL}/api/plans")
        if response.status_code == 200:
            data = response.json()
            print("✅ Plans retrieved successfully")
            print(f"   Total plans: {data['total_plans']}")
            for plan in data['data']:
                print(f"   - {plan['name']}: {plan['interest_rate']} ({plan['term']})")
        else:
            print(f"❌ Failed to get plans: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error getting plans: {e}")
    print()

def test_create_enrollment():
    """Test creating a new enrollment"""
    print("🔍 Testing POST /api/enroll...")
    
    # Test data
    enrollment_data = {
        "name": "John Doe",
        "email": f"john.doe.{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com",
        "phone": "1234567890",
        "address": "123 Main Street, Anytown, ST 12345",
        "selected_plan_id": 1,
        "monthly_contribution": 500.00
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/enroll",
            json=enrollment_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Enrollment created successfully")
            print(f"   Enrollment ID: {data['enrollment_id']}")
            print(f"   Message: {data['message']}")
            return data['enrollment_id']
        else:
            print(f"❌ Failed to create enrollment: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating enrollment: {e}")
        return None

def test_get_enrollment(enrollment_id):
    """Test getting a specific enrollment"""
    if not enrollment_id:
        print("⏭️  Skipping enrollment retrieval (no enrollment ID)")
        return
    
    print(f"🔍 Testing GET /api/enroll/{enrollment_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/enroll/{enrollment_id}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Enrollment retrieved successfully")
            enrollment = data['data']
            print(f"   Name: {enrollment['name']}")
            print(f"   Email: {enrollment['email']}")
            print(f"   Plan: {enrollment['selected_plan']['name']}")
            print(f"   Contribution: ${enrollment['monthly_contribution']}")
        else:
            print(f"❌ Failed to get enrollment: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error getting enrollment: {e}")
    print()

def test_validation_errors():
    """Test API validation by sending invalid data"""
    print("🔍 Testing validation errors...")
    
    # Test with invalid email
    invalid_data = {
        "name": "Test User",
        "email": "invalid-email",
        "phone": "123",
        "address": "Short",
        "selected_plan_id": 999,
        "monthly_contribution": -100
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/enroll",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 422:  # Validation error
            print("✅ Validation working correctly")
            print("   API correctly rejected invalid data")
        elif response.status_code == 400:
            print("✅ Business validation working correctly")
            print(f"   Error: {response.json().get('detail', 'Unknown error')}")
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing validation: {e}")
    print()

def main():
    """Run all tests"""
    print("🚀 Starting API Tests for SecureBank Financial Services")
    print("=" * 60)
    
    # Test basic connectivity
    test_health_check()
    
    # Test plans endpoint
    test_get_plans()
    
    # Test enrollment creation
    enrollment_id = test_create_enrollment()
    print()
    
    # Test enrollment retrieval
    test_get_enrollment(enrollment_id)
    
    # Test validation
    test_validation_errors()
    
    print("🏁 API Tests Completed")
    print("=" * 60)
    print("💡 To view API documentation, visit:")
    print(f"   Swagger UI: {BASE_URL}/docs")
    print(f"   ReDoc: {BASE_URL}/redoc")

if __name__ == "__main__":
    main()
