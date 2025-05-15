"""Команды DLQ."""

from typing import (
    Optional,
)
from uuid import (
    UUID,
)

from explicit.messagebus.commands import (
    Command,
)


class RegisterDeadLetter(Command):
    """Зарегистрировать сообщение, которое не удалось обработать."""

    topic: str
    raw_message_value: bytes
    raw_message_key: Optional[bytes] = None
    exception: Exception

    class Config:  # noqa: D106
        arbitrary_types_allowed = True


class ProcessDeadLetter(Command):
    """Выполнить попытку обработки сообщения."""

    id: UUID


class UpdateDeadLetterRawMessage(ProcessDeadLetter):
    """Обновить содержимое сообщения в DLQ."""

    id: UUID
    raw_message_value: bytes
