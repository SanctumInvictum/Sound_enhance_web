import asyncio
from src.core.rabbit_dependencies import get_rabbitmq_client


async def handle_preprocessing_task(message: dict):
    print("Обработка:", message)
    # здесь извлечение аудио и загрузка в S3


async def main():
    rabbit_client = await get_rabbitmq_client()
    await rabbit_client.consume("preprocessing_queue", callback=handle_preprocessing_task)


if __name__ == "__main__":
    asyncio.run(main())