#!/usr/bin/env python3
"""
Запуск gRPC сервера в отдельном режиме
"""
import asyncio
import logging
import sys

from grpc_server.server import AsyncGRPCServer
from lawly_db.db_models.db_session import global_init


async def main():
    """
    Основная функция запуска сервера
    """
    # Настраиваем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logger = logging.getLogger("grpc_server")

    # Инициализация БД
    logger.info("Инициализация базы данных...")
    await global_init()

    # Порт gRPC сервера
    port = 50051

    # Запуск gRPC сервера
    logger.info(f"Запуск gRPC сервера на порту {port}...")
    server = AsyncGRPCServer(port=port)
    await server.start()

    logger.info(f"gRPC сервер успешно запущен на порту {port}")

    # Ожидание завершения работы сервера
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки...")
        await server.stop(grace=5)
        logger.info("gRPC сервер остановлен")


if __name__ == "__main__":
    asyncio.run(main())
