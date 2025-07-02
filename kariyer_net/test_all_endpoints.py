import requests
from datetime import datetime

API_GATEWAY_URL = "http://api_gateway:8080/api/v1"

def print_section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def test_auth():
    print_section("AUTH ENDPOINTS")
    # Register
    register_data = {
        "email": "testuser@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "phone": "+905551234567",
        "is_company": False
    }
    r = requests.post(f"{API_GATEWAY_URL}/auth/register", json=register_data)
    print("Register:", r.status_code, r.json())
    # Login
    login_data = {"email": "testuser@example.com", "password": "password123"}
    r = requests.post(f"{API_GATEWAY_URL}/auth/login", json=login_data)
    print("Login:", r.status_code, r.json())
    # Profile
    r = requests.get(f"{API_GATEWAY_URL}/auth/profile")
    print("Profile:", r.status_code, r.json())
    # Update profile
    update_data = register_data.copy()
    update_data["first_name"] = "Updated"
    r = requests.put(f"{API_GATEWAY_URL}/auth/profile", json=update_data)
    print("Update profile:", r.status_code, r.json())
    # Refresh token
    r = requests.post(f"{API_GATEWAY_URL}/auth/refresh")
    print("Refresh token:", r.status_code, r.json())
    # Logout
    r = requests.post(f"{API_GATEWAY_URL}/auth/logout")
    print("Logout:", r.status_code, r.json())

def test_jobs():
    print_section("JOBS ENDPOINTS")
    # Search jobs (GET)
    r = requests.get(f"{API_GATEWAY_URL}/jobs/", params={"query": "Python", "location": "Istanbul"})
    print("Search jobs:", r.status_code, r.json())
    # Advanced search (POST)
    search_data = {"query": "Python", "location": "Istanbul", "page": 1, "limit": 5}
    r = requests.post(f"{API_GATEWAY_URL}/jobs/search", json=search_data)
    print("Advanced search:", r.status_code, r.json())
    # Search history
    r = requests.get(f"{API_GATEWAY_URL}/jobs/search/history", params={"user_id": 1})
    print("Search history:", r.status_code, r.json())
    # Search analytics
    r = requests.get(f"{API_GATEWAY_URL}/jobs/search/analytics")
    print("Search analytics:", r.status_code, r.json())
    # Search suggestions
    r = requests.get(f"{API_GATEWAY_URL}/jobs/search/suggestions", params={"query": "Python"})
    print("Search suggestions:", r.status_code, r.json())
    # Get available filters
    r = requests.get(f"{API_GATEWAY_URL}/jobs/search/filters")
    print("Available filters:", r.status_code, r.json())
    # Create job (may require admin/company, may fail)
    job_data = {
        "title": "Test Job",
        "description": "Test job description",
        "company_id": 1,
        "location": "Istanbul",
        "salary_min": 10000,
        "salary_max": 20000,
        "work_mode": "remote",
        "job_type": "full-time"
    }
    r = requests.post(f"{API_GATEWAY_URL}/jobs/", json=job_data)
    print("Create job:", r.status_code, r.json())
    # Get job by ID (mocked)
    r = requests.get(f"{API_GATEWAY_URL}/jobs/1")
    print("Get job by ID:", r.status_code, r.json())
    # Update job (mocked)
    update_data = job_data.copy()
    update_data["title"] = "Updated Job"
    r = requests.put(f"{API_GATEWAY_URL}/jobs/1", json=update_data)
    print("Update job:", r.status_code, r.json())
    # Delete job (mocked)
    r = requests.delete(f"{API_GATEWAY_URL}/jobs/1")
    print("Delete job:", r.status_code, r.json())
    # Save search
    r = requests.post(f"{API_GATEWAY_URL}/jobs/search/save", json=search_data, params={"user_id": 1})
    print("Save search:", r.status_code, r.json())
    # Apply to job
    r = requests.post(f"{API_GATEWAY_URL}/jobs/1/apply", json={"user_id": 1})
    print("Apply to job:", r.status_code, r.json())

def test_notifications():
    print_section("NOTIFICATIONS ENDPOINTS")
    # Create job alert
    alert_data = {
        "user_id": 1,
        "keywords": ["python", "developer"],
        "location": "Istanbul",
        "salary_min": 50000,
        "salary_max": 100000,
        "frequency": "daily"
    }
    r = requests.post(f"{API_GATEWAY_URL}/notifications/alerts", json=alert_data)
    print("Create job alert:", r.status_code, r.json())
    # Get job alerts
    r = requests.get(f"{API_GATEWAY_URL}/notifications/alerts", params={"user_id": 1})
    print("Get job alerts:", r.status_code, r.json())
    # Update job alert
    r = requests.put(f"{API_GATEWAY_URL}/notifications/alerts/1", json=alert_data)
    print("Update job alert:", r.status_code, r.json())
    # Delete job alert
    r = requests.delete(f"{API_GATEWAY_URL}/notifications/alerts/1")
    print("Delete job alert:", r.status_code, r.json())
    # Create notification
    notif_data = {
        "user_id": 1,
        "title": "Test Notification",
        "message": "This is a test notification.",
        "type": "info",
        "priority": "normal"
    }
    r = requests.post(f"{API_GATEWAY_URL}/notifications/notifications", json=notif_data)
    print("Create notification:", r.status_code, r.json())
    # Get notifications
    r = requests.get(f"{API_GATEWAY_URL}/notifications/")
    print("Get notifications:", r.status_code, r.json())
    # Mark notification as read
    r = requests.put(f"{API_GATEWAY_URL}/notifications/notifications/1/read")
    print("Mark notification read:", r.status_code, r.json())
    # Delete notification
    r = requests.delete(f"{API_GATEWAY_URL}/notifications/notifications/1")
    print("Delete notification:", r.status_code, r.json())
    # Send email
    email_data = {
        "to_email": "testuser@example.com",
        "subject": "Test Email",
        "body": "This is a test email."
    }
    r = requests.post(f"{API_GATEWAY_URL}/notifications/email", json=email_data)
    print("Send email:", r.status_code, r.json())
    # Send SMS
    sms_data = {"phone": "+905551234567", "message": "Test SMS message."}
    r = requests.post(f"{API_GATEWAY_URL}/notifications/sms", params=sms_data)
    print("Send SMS:", r.status_code, r.json())
    # Bulk notifications
    bulk_notifs = [notif_data, notif_data]
    r = requests.post(f"{API_GATEWAY_URL}/notifications/notifications/bulk", json=bulk_notifs)
    print("Bulk notifications:", r.status_code, r.json())
    # Bulk mark as read
    r = requests.put(f"{API_GATEWAY_URL}/notifications/notifications/bulk/read", json=[1,2])
    print("Bulk mark as read:", r.status_code, r.json())

def test_ai_agent():
    print_section("AI AGENT ENDPOINTS")
    # Chat
    chat_data = {"user_id": 1, "message": "Find me Python jobs in Istanbul"}
    r = requests.post(f"{API_GATEWAY_URL}/ai_agent/chat", json=chat_data)
    print("AI chat:", r.status_code, r.json())
    # Chat history
    r = requests.get(f"{API_GATEWAY_URL}/ai_agent/chat/history/1")
    print("Chat history:", r.status_code, r.json())
    # Conversation
    r = requests.get(f"{API_GATEWAY_URL}/ai_agent/chat/conversation/conv_123")
    print("Conversation:", r.status_code, r.json())
    # Job recommendations
    r = requests.post(f"{API_GATEWAY_URL}/ai_agent/recommendations/jobs", params={"user_id": 1, "limit": 1})
    print("Job recommendations:", r.status_code, r.json())
    # Skill recommendations
    r = requests.post(f"{API_GATEWAY_URL}/ai_agent/recommendations/skills", json={"user_id": 1, "current_skills": ["Python"]})
    print("Skill recommendations:", r.status_code, r.json())
    # Career advice
    r = requests.get(f"{API_GATEWAY_URL}/ai_agent/career/advice", params={"user_id": 1})
    print("Career advice:", r.status_code, r.json())
    # Career path
    r = requests.post(f"{API_GATEWAY_URL}/ai_agent/career/path", params={"user_id": 1, "current_role": "Developer", "target_role": "Senior Developer"})
    print("Career path:", r.status_code, r.json())
    # Resume analysis
    analysis_data = {"user_id": 1, "resume_text": "Python, Django, FastAPI", "analysis_type": "resume_analysis"}
    r = requests.post(f"{API_GATEWAY_URL}/ai_agent/analysis/resume", json=analysis_data)
    print("Resume analysis:", r.status_code, r.json())
    # Job matching analysis
    r = requests.post(f"{API_GATEWAY_URL}/ai_agent/analysis/job-matching", params={"user_id": 1, "job_description": "Python Developer"})
    print("Job matching analysis:", r.status_code, r.json())
    # Interview prep
    r = requests.get(f"{API_GATEWAY_URL}/ai_agent/interview/prep/1")
    print("Interview prep:", r.status_code, r.json())
    # Practice interview
    r = requests.post(f"{API_GATEWAY_URL}/ai_agent/interview/practice", params={"user_id": 1, "question": "Tell me about yourself."})
    print("Practice interview:", r.status_code, r.json())
    # Market insights
    r = requests.get(f"{API_GATEWAY_URL}/ai_agent/market/insights")
    print("Market insights:", r.status_code, r.json())
    # Learning recommendations
    r = requests.get(f"{API_GATEWAY_URL}/ai_agent/learning/recommendations", params={"user_id": 1, "skill": "Python"})
    print("Learning recommendations:", r.status_code, r.json())

def main():
    print("🧪 API GATEWAY ENDPOINTS TESTING")
    print(f"Testing API Gateway at: {API_GATEWAY_URL}")
    print(f"Timestamp: {datetime.now()}")
    test_auth()
    test_jobs()
    test_notifications()
    test_ai_agent()
    print("\n✅ All main API Gateway endpoints have been tested!")

if __name__ == "__main__":
    main() 