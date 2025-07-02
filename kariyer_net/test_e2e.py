import asyncio
import httpx

API_GATEWAY_URL = "http://job_posting_service:8000"  # Change if your gateway runs elsewhere

async def wait_for_service(url, timeout=60):
    for _ in range(timeout):
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(url)
                if r.status_code == 200:
                    print(f"Service healthy: {url}")
                    return True
        except Exception:
            pass
        await asyncio.sleep(1)
    print(f"Service not healthy: {url}")
    return False

async def main():
    # 1. Wait for all services to be healthy
    await wait_for_service(f"{API_GATEWAY_URL}/health")
    # Add more health checks if you expose them for other services

    async with httpx.AsyncClient() as client:
        # 2. Create a job (example endpoint, adjust as needed)
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
        resp = await client.post(f"{API_GATEWAY_URL}/api/v1/jobs", json=job_data)
        print("Create job:", resp.status_code, resp.json())
        job_id = resp.json().get("id", 1)

        # 3. Search for jobs
        resp = await client.get(f"{API_GATEWAY_URL}/api/v1/search", params={"query": "Python", "location": "Istanbul"})
        print("Search jobs:", resp.status_code, resp.json())

        # 4. Apply to a job
        apply_data = {"user_id": 1}
        resp = await client.post(f"{API_GATEWAY_URL}/api/v1/jobs/{job_id}/apply", json=apply_data)
        print("Apply to job:", resp.status_code, resp.json())

        # 5. Chat with AI agent
        chat_data = {"message": "Find me Python jobs in Istanbul"}
        resp = await client.post(f"{API_GATEWAY_URL}/api/v1/chat", json=chat_data)
        print("AI chat:", resp.status_code, resp.json())

if __name__ == "__main__":
    asyncio.run(main())



