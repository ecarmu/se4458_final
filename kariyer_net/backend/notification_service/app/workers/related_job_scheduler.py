import asyncio 
import requests
import json
from motor.motor_asyncio import AsyncIOMotorClient
import aio_pika
from aio_pika import Message, DeliveryMode
from ..core.queue import get_rabbitmq_connection

# MONGODB_URL     = "mongodb://localhost:27017"
MONGODB_URL     = "mongodb://nosql:27017"
# JOB_SERVICE_URL = "http://job_posting_service:8000/api/v1/jobs/"
JOB_SERVICE_URL = "http://job_posting_service:8000/api/v1/jobs/"

async def fetch_user_searches():
    client = AsyncIOMotorClient(MONGODB_URL)
    db     = client["job_search"]
    user_ids = await db.search_history.distinct("user_id")
    searches = {}
    for uid in user_ids:
        history = await db.search_history\
                          .find({"user_id": uid})\
                          .sort("created_at", -1)\
                          .to_list(length=5)
        searches[uid] = history
    client.close()
    return searches

def fetch_all_jobs():
    resp = requests.get(JOB_SERVICE_URL)
    return resp.json() if resp.status_code == 200 else []

async def scheduler_loop():
    # Open connection once, reuse it
    connection = await get_rabbitmq_connection()
    channel    = await connection.channel()
    queue      = await channel.declare_queue("job.related", durable=True)

    while True:
        print("[RelatedJobScheduler] Checking for related job notifications…")
        searches = await fetch_user_searches()
        jobs     = fetch_all_jobs()

        for user_id, history in searches.items():
            terms = [h["job_name"] for h in history if h.get("job_name")]
            found_any = False

            for job in jobs:
                title = job.get("title", "").lower()
                desc  = job.get("description", "").lower()
                if any(term.lower() in title or term.lower() in desc for term in terms):
                    found_any = True

                    payload = {
                        "user_id": user_id,
                        "job": job
                    }

                    # Publish the notification to RabbitMQ
                    await channel.default_exchange.publish(
                        Message(
                            body=json.dumps(payload).encode(),
                            delivery_mode=DeliveryMode.PERSISTENT,
                        ),
                        routing_key=queue.name,
                    )
                    print(f"[RelatedJobScheduler] Published match for user {user_id} → job {job['id']}")

            if not terms:
                print(f"[RelatedJobScheduler] No search terms for user {user_id}")
            elif not found_any:
                print(f"[RelatedJobScheduler] No related jobs for user {user_id}")

        await asyncio.sleep(300)  # 5 minutes

    # never reached, but good hygiene:
    await connection.close()

if __name__ == "__main__":
    asyncio.run(scheduler_loop())
