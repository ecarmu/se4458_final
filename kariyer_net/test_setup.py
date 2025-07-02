#!/usr/bin/env python3
"""
Comprehensive test script to debug setup issues
"""

import sys
import os
import subprocess
import time
import requests
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import fastapi
        print(f"✅ FastAPI version: {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn version: {uvicorn.__version__}")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy version: {sqlalchemy.__version__}")
    except ImportError as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False
    
    return True

def test_api_gateway_import():
    """Test if API Gateway can be imported"""
    print("\n🔍 Testing API Gateway import...")
    
    # Change to API Gateway directory
    api_gateway_dir = Path("backend/api_gateway")
    if not api_gateway_dir.exists():
        print(f"❌ API Gateway directory not found: {api_gateway_dir}")
        return False
    
    # Add the directory to Python path
    sys.path.insert(0, str(api_gateway_dir))
    
    try:
        from app.main import app
        print("✅ API Gateway app imported successfully")
        return True
    except Exception as e:
        print(f"❌ API Gateway import failed: {e}")
        return False

def test_simple_server():
    """Test a simple FastAPI server"""
    print("\n🔍 Testing simple FastAPI server...")
    
    from fastapi import FastAPI
    import uvicorn
    import threading
    import time
    
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {"message": "Test server working!"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    # Start server in a thread
    def run_server():
        uvicorn.run(app, host="127.0.0.1", port=8082, log_level="error")
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(3)
    
    # Test the server
    try:
        response = requests.get("http://127.0.0.1:8082/", timeout=5)
        if response.status_code == 200:
            print("✅ Simple server test passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        return False

def test_api_gateway_server():
    """Test the actual API Gateway server"""
    print("\n🔍 Testing API Gateway server...")
    
    # Change to API Gateway directory
    api_gateway_dir = Path("backend/api_gateway")
    if not api_gateway_dir.exists():
        print(f"❌ API Gateway directory not found: {api_gateway_dir}")
        return False
    
    # Add the directory to Python path
    sys.path.insert(0, str(api_gateway_dir))
    
    try:
        from app.main import app
        import uvicorn
        import threading
        import time
        
        # Start server in a thread
        def run_server():
            uvicorn.run(app, host="127.0.0.1", port=8083, log_level="error")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        time.sleep(3)
        
        # Test the server
        response = requests.get("http://127.0.0.1:8083/", timeout=5)
        if response.status_code == 200:
            print("✅ API Gateway server test passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ API Gateway server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Gateway server test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting comprehensive setup test...")
    print("=" * 50)
    
    # Test 1: Imports
    if not test_imports():
        print("\n❌ Import test failed. Please check your dependencies.")
        return
    
    # Test 2: API Gateway import
    if not test_api_gateway_import():
        print("\n❌ API Gateway import failed. Please check the code structure.")
        return
    
    # Test 3: Simple server
    if not test_simple_server():
        print("\n❌ Simple server test failed. Please check your network/firewall settings.")
        return
    
    # Test 4: API Gateway server
    if not test_api_gateway_server():
        print("\n❌ API Gateway server test failed. Please check the API Gateway code.")
        return
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Your setup is working correctly.")
    print("\n📝 Next steps:")
    print("1. Install Docker Desktop for Windows")
    print("2. Run: docker compose up --build")
    print("3. Access your services at:")
    print("   - Frontend: http://localhost:3000")
    print("   - API Gateway: http://api_gateway:8080")
    print("   - API Docs: http://api_gateway:8080/docs")

if __name__ == "__main__":
    main() 