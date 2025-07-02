import requests
import random

JOB_POST_URL = "http://job_search_service:8001/api/v1/jobs/"

job_data = {
    "title": f"RabbitMQ Test Job {random.randint(1000, 9999)}",
    "description": "This job should trigger a RabbitMQ event.",
    "company_id": 1,
    "location": "Istanbul, Turkey",
    "salary_min": 50000,
    "salary_max": 80000,
    "work_mode": "remote",
    "job_type": "full-time"
}

print("--- Creating a new job to test RabbitMQ event ---")
resp = requests.post(JOB_POST_URL, json=job_data)
print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}") 