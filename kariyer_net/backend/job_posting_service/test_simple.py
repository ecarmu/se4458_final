#!/usr/bin/env python3
"""
Simple test script for Job Posting Service
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from app.main import app
        print("✅ Main app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_app():
    """Create a simple working app"""
    from fastapi import FastAPI
    
    app = FastAPI(title="Simple Test")
    
    @app.get("/")
    async def root():
        return {"message": "Simple test working"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    return app

if __name__ == "__main__":
    print("🚀 Starting Job Posting Service test...")
    
    if test_imports():
        print("✅ All imports successful!")
        
        # Test simple app
        app = test_simple_app()
        print("✅ Simple app created successfully!")
        
        # Try to run it
        import uvicorn
        print("🚀 Starting server...")
        uvicorn.run(app, host="127.0.0.1", port=8002)
    else:
        print("❌ Import test failed!") 