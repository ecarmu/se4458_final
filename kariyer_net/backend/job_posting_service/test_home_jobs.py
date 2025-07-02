import requests

HOME_JOBS_URL = "http://job_search_service:8001/api/v1/jobs/home"

# Test with a city that likely has jobs
CITY_WITH_JOBS = "Istanbul"
# Test with a city that likely has no jobs (to trigger fallback)
CITY_WITHOUT_JOBS = "NowhereCity"

def print_result(resp):
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}\n")

def test_home_jobs(city):
    print(f"--- Test: Home Jobs for city '{city}' ---")
    params = {"city": city}
    resp = requests.get(HOME_JOBS_URL, params=params)
    print_result(resp)
    return resp

def main():
    test_home_jobs(CITY_WITH_JOBS)
    test_home_jobs(CITY_WITHOUT_JOBS)

if __name__ == "__main__":
    main() 