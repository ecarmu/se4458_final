import requests
import time

SEARCH_URL = "http://notification_service:8002/api/v1/search"
SUGGESTIONS_URL = f"{SEARCH_URL}/suggestions"
HISTORY_URL = f"{SEARCH_URL}/history"

# Test user ID
TEST_USER_ID = 123

def print_result(resp):
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}\n")

def test_search():
    print("--- Test: Search Jobs ---")
    params = {"query": "Software Engineer", "location": "Istanbul", "user_id": TEST_USER_ID}
    resp = requests.get(SEARCH_URL, params=params)
    print_result(resp)
    return resp

def test_autocomplete():
    print("--- Test: Autocomplete Suggestions ---")
    params = {"query": "Soft"}
    resp = requests.get(SUGGESTIONS_URL, params=params)
    print_result(resp)
    return resp

def test_recent_searches():
    print("--- Test: Recent Searches ---")
    params = {"user_id": TEST_USER_ID}
    resp = requests.get(HISTORY_URL, params=params)
    print_result(resp)
    return resp

def main():
    test_search()
    time.sleep(1)
    test_autocomplete()
    time.sleep(1)
    test_recent_searches()

if __name__ == "__main__":
    main() 