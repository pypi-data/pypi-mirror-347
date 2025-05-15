"""Сервисы предметной области для работы с DLQ."""

from typing import (
    Optional,
)

from explicit.unit_of_work import (
    AbstractUnitOfWork,
)

from .factories import (
    DeadLetterDTO,
    factory,
)
from .model import (
    DeadLetter,
)


def register_dead_letter(
    raw_message_value: bytes,
    raw_message_key: Optional[bytes],
    topic: str,
    exception: Exception,
    uow: 'AbstractUnitOfWork',
) -> DeadLetter:
    """Зарегистрировать сообщение в очереди необработанных сообщений."""
    dead_letter = uow.dead_letters.add(  # type: ignore[attr-defined]
        factory.create_from_exception(raw_message_value, raw_message_key, topic, exception)
    )

    return dead_letter


def register_attempt(
    data: DeadLetterDTO,
    exception: Exception,
    uow: 'AbstractUnitOfWork',
) -> DeadLetter:
    """Добавить информацию о новой попытке обработки."""
    dead_letter = uow.dead_letters.get_object_by_id(data.id)  # type: ignore[attr-defined]

    dead_letter.register_attempt(factory.create_attempt_from_exception(exception))

    return uow.dead_letters.update(dead_letter)  # type: ignore[attr-defined]


def mark_as_processed(
    data: DeadLetterDTO,
    uow: 'AbstractUnitOfWork',
) -> DeadLetter:
    """Отметить сообщение как успешно обработанное."""
    dead_letter = uow.dead_letters.get_object_by_id(data.id)  # type: ignore[attr-defined]
    dead_letter.mark_as_processed()

    return uow.dead_letters.update(dead_letter)  # type: ignore[attr-defined]


def update_raw_message(data, uow: 'AbstractUnitOfWork') -> DeadLetter:
    """Редактировать содержимое сообщения в DLQ."""
    dead_letter = uow.dead_letters.get_object_by_id(data.id)  # type: ignore[attr-defined]
    dead_letter.raw_message_value = data.raw_message_value

    return uow.dead_letters.update(dead_letter)  # type: ignore[attr-defined]
