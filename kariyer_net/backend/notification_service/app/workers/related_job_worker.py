import asyncio
import aio_pika
import json
from ..core.queue import get_rabbitmq_connection
from ..services.notification_service import NotificationService
from ..core.database import SessionLocal
from ..schemas.notification import NotificationCreate
from ..models import alert, notification  # Ensure both models are registered

print("RelatedJobWorker starting...")

async def start(self):
    print("Connecting to RabbitMQ...")

class RelatedJobWorker:
    def __init__(self):
        self.db = SessionLocal()
        self.notification_service = NotificationService(self.db)

    def __del__(self):
        self.db.close()

    async def start(self):
        print("Connecting to RabbitMQ...")
        connection = await get_rabbitmq_connection()
        print("Connected to RabbitMQ.")
        channel = await connection.channel()
        queue = await channel.declare_queue("job.related", durable=True)
        print("Declared queue, entering message loop...")
        
        async with queue.iterator() as queue_iter:
            print("Listening for messages...")
            async for message in queue_iter:
                try:
                    print("Message received!")
                    async with message.process():
                        await self.process_related_job(json.loads(message.body.decode()))
                except Exception as e:
                    print("[RelatedJobWorker] Exception while processing message:", e)

    async def process_related_job(self, data: dict):
        """Process related job notification"""
        user_id = data.get('user_id')
        job = data.get('job')

        if not user_id or not job:
            print('[RelatedJobWorker] Missing user_id or job in data:', data)
            return

        print(f"[RelatedJobWorker] Processing related job for user {user_id}: {job.get('title')}")

        notification = NotificationCreate(
            user_id=user_id,
            type="related_job",
            title=f"İlgili İş: {job.get('title', 'Bir iş')} - {job.get('location', '')}",
            message=f"'{job.get('title', 'Bir iş')}' başlıklı bir iş ilanı ilginizi çekebilir!",
            data={"job_id": job.get('id')}
        )
        await self.notification_service.create_notification(notification)


    
if __name__ == "__main__":
    worker = RelatedJobWorker()
    import asyncio
    try:
        asyncio.run(worker.start())
    except Exception as e:
        print("Worker crashed with exception:", e)