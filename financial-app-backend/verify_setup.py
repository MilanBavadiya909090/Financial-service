#!/usr/bin/env python3
"""
Verification script to check if the backend setup is correct
"""

import sys
import os

def check_imports():
    """Check if all required modules can be imported"""
    print("🔍 Checking imports...")
    
    try:
        import fastapi
        print(f"✅ FastAPI: {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn: {uvicorn.__version__}")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import pydantic
        print(f"✅ Pydantic: {pydantic.__version__}")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        return False
    
    return True

def check_app_structure():
    """Check if the application structure is correct"""
    print("\n🔍 Checking application structure...")
    
    required_files = [
        "main.py",
        "app/__init__.py",
        "app/models/schemas.py",
        "app/data/financial_plans.py",
        "app/services/enrollment_service.py",
        "app/routers/plans.py",
        "app/routers/enrollment.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    return True

def check_app_import():
    """Check if the main app can be imported"""
    print("\n🔍 Checking main app import...")
    
    try:
        from main import app
        print("✅ Main app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import main app: {e}")
        return False

def main():
    """Run all verification checks"""
    print("🏦 SecureBank Financial Services - Backend Verification")
    print("=" * 60)
    
    # Change to the correct directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    checks = [
        check_imports,
        check_app_structure,
        check_app_import
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All checks passed! Backend is ready to run.")
        print("\n💡 To start the server, run:")
        print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("\n📚 API Documentation will be available at:")
        print("   http://localhost:8000/docs")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
