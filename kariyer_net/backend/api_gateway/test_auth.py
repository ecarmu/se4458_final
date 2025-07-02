import requests
import json

# Test the auth endpoint
url = "http://api_gateway:8080/api/v1/auth/login"
data = {
    "email": "test@test.com",
    "password": "test"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}") 