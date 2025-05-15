"""Типы для работы с DLQ."""

from typing import (
    Protocol,
)


class DLQMessageDispatcher(Protocol):
    """Протокол обработчика сообщений DLQ.

    Получает сырое сообщение и топик, трансформирует его в событие предметной области и направляет в шину на обработку.
    """

    def __call__(self, raw_message_value: bytes, topic: str) -> None:
        """Обработать сообщение."""
