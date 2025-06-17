import json
from aio_pika import connect_robust, Message, IncomingMessage, ExchangeType
from typing import Callable


class AsyncRabbitMQClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connection = None
        self.channel = None
        self.queues = {}

    async def connect(self):
        self.connection = await connect_robust(host=self.host, port=self.port)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

    async def declare_queue(self, queue_name: str):
        if not self.channel:
            await self.connect()
        queue = await self.channel.declare_queue(queue_name, durable=True)
        self.queues[queue_name] = queue
        return queue

    async def send(self, message: dict, queue_name: str):
        if not self.channel:
            await self.connect()
        await self.declare_queue(queue_name)
        msg = Message(
            body=json.dumps(message).encode(),
            delivery_mode=2  # persistent
        )
        await self.channel.default_exchange.publish(msg, routing_key=queue_name)

    async def consume(self, queue_name: str, callback: Callable[[dict], None]):
        if not self.channel:
            await self.connect()
        queue = await self.declare_queue(queue_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        body = json.loads(message.body.decode())
                        await callback(body)
                    except Exception as e:
                        print(f"Ошибка обработки сообщения: {e}")

    async def close(self):
        if self.connection:
            await self.connection.close()