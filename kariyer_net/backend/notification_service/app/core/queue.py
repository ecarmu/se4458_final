import aio_pika
from .config import settings

async def get_rabbitmq_connection():
    """Get RabbitMQ connection"""
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    return connection 