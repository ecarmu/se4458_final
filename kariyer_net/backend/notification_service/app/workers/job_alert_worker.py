import asyncio
import aio_pika
import json
from ..core.queue import get_rabbitmq_connection
from ..services.alert_service import AlertService
from ..core.database import SessionLocal
from ..services.notification_service import NotificationService
from ..schemas.notification import NotificationCreate

print("JobAlertWorker starting...")

class JobAlertWorker:
    def __init__(self):
        self.db = SessionLocal()
        self.alert_service = AlertService(self.db)
        self.notification_service = NotificationService(self.db)

    def __del__(self):
        self.db.close()

    async def start(self):
        """Start the job alert worker"""
        print("Connecting to RabbitMQ...")
        connection = await get_rabbitmq_connection()
        print("Connected to RabbitMQ.")
        channel = await connection.channel()
        
        # Declare queue (should match producer: 'new_jobs')
        queue = await channel.declare_queue("new_jobs", durable=True)
        
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await self.process_job_created(json.loads(message.body.decode()))

    async def process_job_created(self, job_data: dict):
        """Process new job created event and notify users with matching alerts (assignment requirement)"""
        print(f"[JobAlertWorker] New job received: {job_data}")
        alerts = self.alert_service.get_all_active_alerts()
        notified_users = []
        for alert in alerts:
            # Simplified matching: job name and location (case-insensitive substring)
            if (alert.job_name.lower() in job_data["title"].lower() and
                alert.location.lower() in job_data["location"].lower()):
                print(f"[JobAlertWorker] Notifying user {alert.user_id} about job {job_data['id']}")
                notified_users.append(alert.user_id)
                # Create notification
                notification = NotificationCreate(
                    user_id=alert.user_id,
                    type="job_alert",
                    title=f"Yeni İş: {job_data['title']} - {job_data['location']}",
                    message=f"'{job_data['title']}' başlıklı yeni bir iş ilanı yayınlandı!",
                    data={"job_id": job_data["id"], "alert_id": alert.id}
                )
                await self.notification_service.create_notification(notification)
        if not notified_users:
            print("[JobAlertWorker] No matching alerts for this job.")

if __name__ == "__main__":
    worker = JobAlertWorker()
    asyncio.run(worker.start()) 