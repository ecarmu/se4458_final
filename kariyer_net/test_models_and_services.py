#!/usr/bin/env python3
"""
Test script to verify models and services are working correctly
"""

import sys
import os
import requests
from pathlib import Path

# Add backend directories to Python path
sys.path.insert(0, str(Path("backend/api_gateway/app/models")))
sys.path.insert(0, str(Path("backend/job_posting_service/app/models")))
sys.path.insert(0, str(Path("backend/job_search_service/app/models")))
sys.path.insert(0, str(Path("backend/notification_service/app/models")))

def test_model_imports():
    print("\n🔍 Testing Model Imports...")
    try:
        from user import User
        print("✅ User model imported successfully")
        from company import Company
        print("✅ Company model imported successfully")
        from job import Job
        print("✅ Job model imported successfully")
        from application import JobApplication
        print("✅ JobApplication model imported successfully")
        from search_history import SearchHistory
        print("✅ SearchHistory model imported successfully")
        from notification import Notification
        print("✅ Notification model imported successfully")
        from alert import JobAlert
        print("✅ JobAlert model imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Model import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during model import: {e}")
        return False

def test_model_creation():
    print("\n🔍 Testing Model Creation...")
    try:
        from user import User
        user = User(id=1, email="test@example.com", password="testpassword", search_history={}, notifications={})
        print("✅ User model created successfully")
        from company import Company
        company = Company(id=1, name="Test Company", logo_url="https://example.com/logo.png", location="Istanbul", jobs="[1,2,3]")
        print("✅ Company model created successfully")
        from job import Job
        job = Job(id=1, job_name="Yazılım Uzmanı", country="Turkey", city="Istanbul", town="Kadıköy", employment_type="full-time", workplace_type="hybrid", company_id=1, job_description="desc")
        print("✅ Job model created successfully")
        from search_history import SearchHistory
        sh = SearchHistory(id=1, user_id=1, job_name="Yazılım Uzmanı", location="Istanbul", employment_type="full-time")
        print("✅ SearchHistory model created successfully")
        from alert import JobAlert
        alert = JobAlert(id=1, user_id=1, job_name="Yazılım Uzmanı", location="Istanbul", employment_type="full-time", is_active=True)
        print("✅ JobAlert model created successfully")
        return True
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return False

def test_service_health():
    print("\n🔍 Testing Service Health...")
    services = {
        "API Gateway": "http://api_gateway:8080",
        "Job Posting Service": "http://localhost:8081",
        "Job Search Service": "http://localhost:8082",
        "Notification Service": "http://localhost:8083",
        "AI Agent Service": "http://localhost:8084"
    }
    all_healthy = True
    for service_name, url in services.items():
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} is healthy")
            else:
                print(f"❌ {service_name} returned status {response.status_code}")
                all_healthy = False
        except requests.exceptions.RequestException as e:
            print(f"❌ {service_name} is not running: {e}")
            all_healthy = False
    return all_healthy

def main():
    print("\n🚀 Starting Model and Service Tests...")
    print("=" * 50)
    if not test_model_imports():
        print("\n❌ Model import test failed!")
        return
    if not test_model_creation():
        print("\n❌ Model creation test failed!")
        return
    if not test_service_health():
        print("\n⚠️ Some services are not running. Please start them first.")
        return
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\n📝 Summary:")
    print("- Models are properly defined and can be imported")
    print("- Models can be instantiated with sample data")
    print("- Services are running and healthy")
    print("\n🎉 Your models are working and connected to services!")

if __name__ == "__main__":
    main() 