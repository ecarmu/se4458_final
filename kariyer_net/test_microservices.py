import requests
from datetime import datetime

API_GATEWAY_URL = "http://api_gateway:8080/api/v1"

def print_section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def test_auth():
    print_section("AUTHENTICATION TESTS")
    # Login
    login_data = {"email": "test@example.com", "password": "password123"}
    r = requests.post(f"{API_GATEWAY_URL}/auth/login", json=login_data)
    print("Login:", r.status_code, r.json())
    # Register
    register_data = {
        "email": "newuser@example.com",
        "password": "password123",
        "first_name": "Jane",
        "last_name": "Smith",
        "phone": "+905551234567"
    }
    r = requests.post(f"{API_GATEWAY_URL}/auth/register", json=register_data)
    print("Register:", r.status_code, r.json())

def test_job_search_and_crud():
    print_section("JOB SEARCH & CRUD TESTS")
    # Search jobs
    r = requests.get(f"{API_GATEWAY_URL}/jobs/", params={"query": "Python", "location": "Istanbul"})
    print("Search jobs:", r.status_code, r.json())
    jobs = r.json()
    job_id = jobs[0]["id"] if jobs and isinstance(jobs, list) and "id" in jobs[0] else None

    # Create job (requires admin/company user, may fail if not implemented)
    job_data = {
        "title": "Junior Python Developer",
        "description": "Entry level position",
        "company_id": 1,
        "location": "Istanbul",
        "salary_min": 10000,
        "salary_max": 20000,
        "work_mode": "remote",
        "job_type": "full-time"
    }
    r = requests.post(f"{API_GATEWAY_URL}/jobs/", json=job_data)
    print("Create job:", r.status_code, r.json())

    # Apply to job
    if job_id:
        apply_data = {"user_id": 1}
        r = requests.post(f"{API_GATEWAY_URL}/jobs/{job_id}/apply/", json=apply_data)
        print(f"{API_GATEWAY_URL}/jobs/{job_id}/apply/")
        print("Apply to job:", r.status_code, r.json())
    else:
        print("No job found to apply to.")

def test_notifications():
    print_section("NOTIFICATION SERVICE TESTS")
    # Get notifications (proxy)
    r = requests.get(f"{API_GATEWAY_URL}/notifications/")
    print("Get notifications:", r.status_code, r.json())

def test_ai_agent():
    print_section("AI AGENT TESTS")
    # Chat with AI agent (proxy)
    chat_data = {"user_id": 1, "message": "Find me Python jobs in Istanbul"}
    r = requests.post(f"{API_GATEWAY_URL}/ai_agent/chat", json=chat_data)
    print(f"{API_GATEWAY_URL}/ai_agent/chat")
    print("AI chat:", r.status_code, r.json())

def main():
    print("🧪 MICROSERVICES API GATEWAY TESTING")
    print(f"Testing API Gateway at: {API_GATEWAY_URL}")
    print(f"Timestamp: {datetime.now()}")
    test_auth()
    test_job_search_and_crud()
    test_notifications()
    test_ai_agent()
    print("\n✅ All main API Gateway endpoints have been tested!")

if __name__ == "__main__":
    main() 