import requests

BASE_URL = "http://job_search_service:8001/api/v1/jobs"
TEST_USER_ID = 123

# Use a job ID that exists in your system
TEST_JOB_ID = 1


def print_result(resp):
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}\n")

def test_job_details(job_id):
    print(f"--- Test: Job Details for job_id={job_id} ---")
    resp = requests.get(f"{BASE_URL}/{job_id}")
    print_result(resp)
    return resp

def test_related_jobs(job_id):
    print(f"--- Test: Related Jobs for job_id={job_id} ---")
    resp = requests.get(f"{BASE_URL}/{job_id}/related")
    print_result(resp)
    return resp

def test_apply_to_job(job_id, user_id):
    print(f"--- Test: Apply to Job job_id={job_id}, user_id={user_id} ---")
    data = {"user_id": user_id}
    resp = requests.post(f"{BASE_URL}/{job_id}/apply", json=data)
    print_result(resp)
    return resp

def main():
    test_job_details(TEST_JOB_ID)
    test_related_jobs(TEST_JOB_ID)
    test_apply_to_job(TEST_JOB_ID, TEST_USER_ID)
    # Try to apply again to test duplicate application
    test_apply_to_job(TEST_JOB_ID, TEST_USER_ID)

if __name__ == "__main__":
    main() 