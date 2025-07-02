import requests
import json

GATEWAY_URL = "http://api_gateway:8080/api/v1/auth"
JOB_POSTING_URL = "http://job_search_service:8001/api/v1/jobs"

# Test users with unique emails
test_users = [
    {"email": "freshuser@example.com", "password": "userpass", "first_name": "User", "last_name": "Test", "is_admin": False, "is_company": False},
    {"email": "freshadmin@example.com", "password": "adminpass", "first_name": "Admin", "last_name": "User", "is_admin": True, "is_company": False},
    {"email": "companyuser@example.com", "password": "companypass", "first_name": "Company", "last_name": "User", "is_admin": False, "is_company": True},
]

def register_and_login(user):
    """Register user and login, handle existing user case"""
    try:
        # Try to register first
        register_resp = requests.post(f"{GATEWAY_URL}/register", json=user)
        if register_resp.status_code == 400 and "already exists" in register_resp.text:
            print(f"User {user['email']} already exists, skipping registration")
        elif register_resp.status_code != 200:
            print(f"Registration failed for {user['email']}: {register_resp.status_code} - {register_resp.text}")
            return None
        
        # Login
        login_resp = requests.post(f"{GATEWAY_URL}/login", json={"email": user["email"], "password": user["password"]})
        if login_resp.status_code == 200:
            token = login_resp.json().get("access_token")
            user_type = "admin" if user['is_admin'] else ("company" if user['is_company'] else "user")
            print(f"Login as {user_type}: {login_resp.status_code}, token: {token[:50]}..." if token else "None")
            return token
        else:
            print(f"Login failed for {user['email']}: {login_resp.status_code} - {login_resp.text}")
            return None
            
    except Exception as e:
        print(f"Error in register_and_login for {user['email']}: {e}")
        return None

def try_job_action(token, method, url, data=None):
    """Try job action with proper error handling"""
    if not token:
        print(f"{method.upper()} {url} -> SKIP (no token)")
        return None
        
    headers = {"Authorization": f"Bearer {token}"}
    try:
        if method == "post":
            resp = requests.post(url, json=data, headers=headers)
        elif method == "put":
            resp = requests.put(url, json=data, headers=headers)
        elif method == "delete":
            resp = requests.delete(url, headers=headers)
        else:
            return None
            
        print(f"{method.upper()} {url} -> {resp.status_code}, {resp.text}")
        return resp
        
    except Exception as e:
        print(f"{method.upper()} {url} -> ERROR: {e}")
        return None

def create_test_job(admin_token):
    """Create a test job for update/delete operations"""
    if not admin_token:
        print("❌ No admin token available to create test job")
        return None
    
    job_data = {
        "title": "Test Job for Update/Delete",
        "description": "This is a test job that will be used for update and delete operations.",
        "company_id": 1,
        "location": "Test Location",
        "salary_min": 30000,
        "salary_max": 50000,
        "work_mode": "remote",
        "job_type": "full-time"
    }
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    try:
        resp = requests.post(f"{JOB_POSTING_URL}/", json=job_data, headers=headers)
        if resp.status_code == 200:
            job = resp.json()
            print(f"✅ Created test job with ID: {job.get('id')}")
            return job.get('id')
        else:
            print(f"❌ Failed to create test job: {resp.status_code} - {resp.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating test job: {e}")
        return None

def main():
    print("🧪 Testing Admin vs User vs Company Job Permissions")
    print("=" * 50)
    
    # Register and login users
    tokens = []
    for user in test_users:
        token = register_and_login(user)
        tokens.append(token)
    
    if not any(tokens):
        print("❌ No valid tokens obtained. Cannot test job operations.")
        return
    
    # Get admin and company tokens
    admin_token = None
    company_token = None
    for i, user in enumerate(test_users):
        if user.get("is_admin"):
            admin_token = tokens[i]
        if user.get("is_company"):
            company_token = tokens[i]
    
    # Complete job data with all required fields
    job_data = {
        "title": "Software Engineer",
        "description": "We are looking for a talented software engineer to join our team and help build amazing products.",
        "company_id": 1,  # Required field
        "location": "Istanbul, Turkey",
        "salary_min": 50000,
        "salary_max": 80000,
        "work_mode": "hybrid",  # Required: remote|on-site|hybrid
        "job_type": "full-time"  # Required: full-time|part-time|contract
    }
    
    # Try to add job as user, admin, and company
    print("\n--- Add Job ---")
    for i, token in enumerate(tokens):
        user_type = "admin" if test_users[i]['is_admin'] else ("company" if test_users[i]['is_company'] else "user")
        print(f"\nTrying as {user_type}:")
        try_job_action(token, "post", JOB_POSTING_URL + "/", job_data)
    
    # Create a test job for update/delete operations (prefer admin, fallback to company)
    print("\n--- Creating Test Job for Update/Delete ---")
    test_job_id = create_test_job(admin_token or company_token)
    
    if test_job_id:
        # Try to update job as user, admin, and company
        print(f"\n--- Update Job (id={test_job_id}) ---")
        update_data = {
            "title": "Senior Software Engineer",
            "description": "Updated job description for senior position.",
            "salary_min": 70000,
            "salary_max": 100000
        }
        for i, token in enumerate(tokens):
            user_type = "admin" if test_users[i]['is_admin'] else ("company" if test_users[i]['is_company'] else "user")
            print(f"\nTrying as {user_type}:")
            try_job_action(token, "put", f"{JOB_POSTING_URL}/{test_job_id}", update_data)
        
        # Try to delete job as user, admin, and company
        print(f"\n--- Delete Job (id={test_job_id}) ---")
        for i, token in enumerate(tokens):
            user_type = "admin" if test_users[i]['is_admin'] else ("company" if test_users[i]['is_company'] else "user")
            print(f"\nTrying as {user_type}:")
            try_job_action(token, "delete", f"{JOB_POSTING_URL}/{test_job_id}")
    else:
        print("⚠️  Skipping update/delete tests because test job creation failed")

if __name__ == "__main__":
    main() 