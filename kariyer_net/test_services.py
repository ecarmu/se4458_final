#!/usr/bin/env python3
"""
Test script to verify all services are working
"""

import requests
import time
import subprocess
import sys
from typing import Dict, List

# Service URLs
SERVICES = {
    "api_gateway": "http://api_gateway:8080",
    "job_posting": "http://job_posting_service:8000", 
    "job_search": "http://job_search_service:8001",
    "notification": "http://notification_service:8002",
    "ai_agent": "http://localhost:8003"
}

def test_service_health(service_name: str, url: str) -> bool:
    """Test if a service is healthy"""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ {service_name}: Healthy")
            return True
        else:
            print(f"❌ {service_name}: Unhealthy (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {service_name}: Connection failed - {e}")
        return False

def test_service_root(service_name: str, url: str) -> bool:
    """Test service root endpoint"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {service_name}: Root endpoint working")
            return True
        else:
            print(f"❌ {service_name}: Root endpoint failed (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {service_name}: Root endpoint failed - {e}")
        return False

def test_api_docs(service_name: str, url: str) -> bool:
    """Test if API docs are accessible"""
    try:
        response = requests.get(f"{url}/docs", timeout=5)
        if response.status_code == 200:
            print(f"✅ {service_name}: API docs accessible")
            return True
        else:
            print(f"❌ {service_name}: API docs failed (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {service_name}: API docs failed - {e}")
        return False

def test_docker_services():
    """Test if Docker services are running"""
    try:
        result = subprocess.run(
            ["docker-compose", "ps"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            print("✅ Docker Compose services:")
            print(result.stdout)
            return True
        else:
            print("❌ Docker Compose failed")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("❌ Docker Compose timeout")
        return False
    except FileNotFoundError:
        print("❌ Docker Compose not found")
        return False

def main():
    """Main test function"""
    print("Testing Job Search Application Services")
    print("=" * 50)
    
    # Test Docker services
    print("\n📦 Testing Docker Services:")
    docker_ok = test_docker_services()
    
    if not docker_ok:
        print("\n❌ Docker services not running. Please start them first:")
        print("docker-compose up -d")
        return
    
    # Wait for services to start
    print("\n⏳ Waiting for services to start...")
    time.sleep(10)
    
    # Test each service
    print("\nTesting Individual Services:")
    results = {}
    
    for service_name, url in SERVICES.items():
        print(f"\n--- Testing {service_name} ---")
        health_ok = test_service_health(service_name, url)
        root_ok = test_service_root(service_name, url)
        docs_ok = test_api_docs(service_name, url)
        
        results[service_name] = {
            "health": health_ok,
            "root": root_ok,
            "docs": docs_ok
        }
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for service_name, result in results.items():
        status = "✅ PASS" if all(result.values()) else "❌ FAIL"
        print(f"{service_name}: {status}")
        if not all(result.values()):
            all_passed = False
    
    if all_passed:
        print("\n🎉 All services are working correctly!")
        print("\nYou can now access:")
        print("- Frontend: http://localhost:3000")
        print("- API Gateway: http://api_gateway:8080")
        print("- Job Posting API: http://job_posting_service:8000/docs")
        print("- Job Search API: http://job_search_service:8001/docs")
        print("- Notification API: http://notification_service:8002/docs")
        print("- AI Agent API: http://localhost:8003/docs")
        print("- RabbitMQ Management: http://localhost:15672")
    else:
        print("\n⚠️  Some services failed. Check the logs above.")
        print("\n🔧 Troubleshooting:")
        print("1. Check if all services are running: docker-compose ps")
        print("2. View logs: docker-compose logs [service-name]")
        print("3. Restart services: docker-compose restart")

if __name__ == "__main__":
    main() 