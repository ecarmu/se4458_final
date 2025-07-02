import asyncio
import httpx
from datetime import datetime, timedelta

async def test_date_filter():
    """Test date filtering functionality"""
    
    # Test with job posting service
    JOB_POSTING_SERVICE_URL = "http://job_posting_service:8000"
    
    try:
        async with httpx.AsyncClient() as client:
            # Get all jobs from job posting service
            resp = await client.get(f"{JOB_POSTING_SERVICE_URL}/api/v1/jobs/")
            resp.raise_for_status()
            all_jobs = resp.json()
            
            print(f"Total jobs found: {len(all_jobs)}")
            
            # Check if jobs have created_at field
            jobs_with_date = [job for job in all_jobs if job.get('created_at')]
            print(f"Jobs with created_at: {len(jobs_with_date)}")
            
            if jobs_with_date:
                print("Sample job with date:")
                sample_job = jobs_with_date[0]
                print(f"  ID: {sample_job.get('id')}")
                print(f"  Title: {sample_job.get('title')}")
                print(f"  Created at: {sample_job.get('created_at')}")
                
                # Test date parsing
                try:
                    created_at = sample_job.get('created_at')
                    if 'T' in created_at:
                        job_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    else:
                        job_date = datetime.fromisoformat(created_at)
                    
                    now = datetime.now(job_date.tzinfo)
                    print(f"  Parsed date: {job_date}")
                    print(f"  Current time: {now}")
                    print(f"  Is today: {job_date.date() == now.date()}")
                    print(f"  Hours ago: {(now - job_date).total_seconds() / 3600:.2f}")
                    
                except Exception as e:
                    print(f"  Date parsing error: {e}")
            else:
                print("No jobs have created_at field!")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_date_filter()) 