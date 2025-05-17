import grpc
import logging
from typing import Optional

from lawly_db.db_models.db_session import create_session

from api import router
from protos.user_service import user_service_pb2 as user_pb2
from protos.user_service import user_service_pb2_grpc as user_pb2_grpc
from services.subscribe_service import SubscribeService
from services.user_service import UserService
from modules.users.enum import GetUserInfoEnum


class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    """
    Реализация GRPC сервиса для работы с пользователями (асинхронная версия)
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._session_factory = None

    async def GetUserInfo(self, request, context):
        """
        Получение информации о пользователе и его подписке
        """
        try:
            user_id = request.user_id
            self.logger.info(f"GRPC запрос GetUserInfo для пользователя {user_id}")

            # Создаем новую сессию для запроса
            async with create_session() as session:
                # Создаем сервисы с новой сессией
                user_service = UserService(session)
                subscribe_service = SubscribeService(session)

                # Получаем информацию о пользователе через существующий сервис
                user_info = await user_service.get_user_info_service(user_id=user_id)

                # Проверяем результат
                if user_info == GetUserInfoEnum.ACCESS_DENIED:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Пользователь не найден")
                    return user_pb2.UserInfoResponse()

                if user_info == GetUserInfoEnum.NOT_SUBSCRIBED:
                    context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
                    context.set_details("У пользователя нет подписки")
                    return user_pb2.UserInfoResponse()

                # Создаем объект тарифа напрямую через конструктор
                tariff = user_pb2.Tariff(
                    id=user_info.tariff.id,
                    name=user_info.tariff.name,
                    description=user_info.tariff.description or "",
                    price=user_info.tariff.price,
                    features=user_info.tariff.features or [],
                )

                # Получаем подписку пользователя для дополнительной информации
                subscription = await subscribe_service.get_user_subscription_service(
                    user_id=user_id
                )

                # Формируем ответ через конструктор
                response_args = {
                    "user_id": user_info.user_id,
                    "tariff": tariff,
                    "start_date": user_info.start_date.isoformat(),
                    "end_date": user_info.end_date.isoformat()
                    if user_info.end_date
                    else None,
                }

                if subscription not in (
                    GetUserInfoEnum.ACCESS_DENIED,
                    GetUserInfoEnum.NOT_SUBSCRIBED,
                ):
                    response_args.update(
                        {
                            "count_lawyers": subscription.count_lawyers,
                            "consultations_total": subscription.consultations_total,
                            "consultations_used": subscription.consultations_used,
                            "can_user_ai": subscription.can_user_ai,
                            "can_create_custom_templates": subscription.can_create_custom_templates,
                            "unlimited_documents": subscription.unlimited_documents,
                        }
                    )

                return user_pb2.UserInfoResponse(**response_args)

        except Exception as e:
            self.logger.error(
                f"Ошибка при обработке GRPC запроса GetUserInfo: {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Внутренняя ошибка сервера: {str(e)}")
            return user_pb2.UserInfoResponse()


class AsyncGRPCServer:
    """
    Класс-обертка для запуска асинхронного GRPC сервера
    """

    def __init__(self, port: int = 50051):
        self.port = port
        self.server = None
        self.logger = logging.getLogger(__name__)

    async def initialize_db(self):
        """
        Инициализация базы данных
        """
        from lawly_db.db_models.db_session import global_init

        await global_init()

    async def start(self):
        """
        Запуск асинхронного GRPC сервера
        """
        # Инициализируем БД
        await self.initialize_db()

        # Создаем экземпляр асинхронного сервера
        self.server = grpc.aio.server()

        # Создаем сервисер и добавляем его на сервер
        servicer = UserServiceServicer()
        user_pb2_grpc.add_UserServiceServicer_to_server(servicer, self.server)

        # Добавляем порт для прослушивания
        listen_addr = f'[::]:{self.port}'
        self.server.add_insecure_port(listen_addr)

        # Запускаем сервер
        await self.server.start()
        self.logger.info(f"Асинхронный GRPC сервер запущен на порту {self.port}")

        return self

    async def stop(self, grace: Optional[float] = None):
        """
        Остановка GRPC сервера

        Args:
            grace: период ожидания в секундах перед принудительной остановкой
        """
        if self.server:
            await self.server.stop(grace)
            self.logger.info("GRPC сервер остановлен")

    async def wait_for_termination(self):
        """
        Ожидание завершения работы сервера
        """
        if self.server:
            await self.server.wait_for_termination()


# Функция для запуска асинхронного сервера
async def run_server():
    router
    server = AsyncGRPCServer()
    await server.start()
    await server.wait_for_termination()
