import requests
import time

JOB_POSTING_URL = "http://job_search_service:8001/api/v1/jobs"

# Dummy token for testing (replace with a real one if auth is enforced)
DUMMY_TOKEN = "testtoken"
HEADERS = {"Authorization": f"Bearer {DUMMY_TOKEN}"}

def print_result(resp):
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}\n")

def test_create_job():
    print("--- Test: Create Job ---")
    job_data = {
        "title": "Redis Test Job",
        "description": "Testing Redis caching for job postings.",
        "company_id": 1,
        "location": "Redis City",
        "salary_min": 10000,
        "salary_max": 20000,
        "work_mode": "remote",
        "job_type": "full-time"
    }
    resp = requests.post(f"{JOB_POSTING_URL}/", json=job_data, headers=HEADERS)
    print_result(resp)
    return resp.json().get("id") if resp.status_code == 200 else None

def test_get_job(job_id):
    print("--- Test: Get Job ---")
    resp = requests.get(f"{JOB_POSTING_URL}/{job_id}", headers=HEADERS)
    print_result(resp)

def test_update_job(job_id):
    print("--- Test: Update Job ---")
    update_data = {
        "title": "Redis Test Job Updated",
        "salary_min": 15000
    }
    resp = requests.put(f"{JOB_POSTING_URL}/{job_id}", json=update_data, headers=HEADERS)
    print_result(resp)

def test_delete_job(job_id):
    print("--- Test: Delete Job ---")
    resp = requests.delete(f"{JOB_POSTING_URL}/{job_id}", headers=HEADERS)
    print_result(resp)

def test_get_deleted_job(job_id):
    print("--- Test: Get Deleted Job (Should be inactive) ---")
    resp = requests.get(f"{JOB_POSTING_URL}/{job_id}", headers=HEADERS)
    print_result(resp)

def main():
    job_id = test_create_job()
    if not job_id:
        print("❌ Failed to create job. Aborting test.")
        return
    time.sleep(1)
    test_get_job(job_id)
    time.sleep(1)
    test_update_job(job_id)
    time.sleep(1)
    test_get_job(job_id)
    time.sleep(1)
    test_delete_job(job_id)
    time.sleep(1)
    test_get_deleted_job(job_id)

if __name__ == "__main__":
    main() 