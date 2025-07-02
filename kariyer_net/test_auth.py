import requests
import json

# Base URL
base_url = "http://api_gateway:8080/api/v1"

def test_login():
    """Test login endpoint"""
    url = f"{base_url}/auth/login"
    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Login Response ({response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Login Error: {e}")
        return False

def test_register():
    """Test register endpoint"""
    url = f"{base_url}/auth/register"
    data = {
        "email": "newuser@example.com",
        "password": "password123",
        "first_name": "Jane",
        "last_name": "Smith",
        "phone": "+1234567890"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"\nRegister Response ({response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Register Error: {e}")
        return False

def test_profile():
    """Test profile endpoint"""
    url = f"{base_url}/auth/profile"
    
    try:
        response = requests.get(url)
        print(f"\nProfile Response ({response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Profile Error: {e}")
        return False

def test_update_profile():
    """Test profile update endpoint"""
    url = f"{base_url}/auth/profile"
    data = {
        "email": "updated@example.com",
        "password": "newpassword123",
        "first_name": "Updated",
        "last_name": "User",
        "phone": "+9876543210"
    }
    
    try:
        response = requests.put(url, json=data)
        print(f"\nUpdate Profile Response ({response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Update Profile Error: {e}")
        return False

def test_refresh_token():
    """Test token refresh endpoint"""
    url = f"{base_url}/auth/refresh"
    
    try:
        response = requests.post(url)
        print(f"\nRefresh Token Response ({response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Refresh Token Error: {e}")
        return False

def test_logout():
    """Test logout endpoint"""
    url = f"{base_url}/auth/logout"
    
    try:
        response = requests.post(url)
        print(f"\nLogout Response ({response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Logout Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Auth Endpoints...")
    print("=" * 50)
    
    # Test all endpoints
    tests = [
        ("Login", test_login),
        ("Register", test_register),
        ("Profile", test_profile),
        ("Update Profile", test_update_profile),
        ("Refresh Token", test_refresh_token),
        ("Logout", test_logout)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print("=" * 50)
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(success for _, success in results)
    print(f"\nOverall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}") 