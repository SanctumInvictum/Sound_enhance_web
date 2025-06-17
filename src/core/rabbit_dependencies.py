from src.services.rabbit_client import AsyncRabbitMQClient
from src.config import settings


QUEUE_REGISTRY = [
    "preprocessing_queue",
    "processing_queue",
    "postprocessing_queue",
]


async def get_rabbitmq_client() -> AsyncRabbitMQClient:
    if not hasattr(get_rabbitmq_client, "client"):
        client = AsyncRabbitMQClient(
            host=settings.RABBIT_HOST,
            port=settings.RABBIT_PORT
        )
        await client.connect()
        get_rabbitmq_client.client = client
    return get_rabbitmq_client.client


async def init_rabbit_queues():
    client = await get_rabbitmq_client()
    for queue_name in QUEUE_REGISTRY:
        await client.declare_queue(queue_name)