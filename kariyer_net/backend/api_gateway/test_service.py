#!/usr/bin/env python3
"""
Simple test script for API Gateway
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting API Gateway service...")
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True) 