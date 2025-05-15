"""Агрегаты и сущности для работы с недоставленными сообщениями."""

import uuid
from datetime import (
    datetime,
    timezone,
)
from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
)

from pydantic import (
    Field,
    validator,
)

from explicit.contrib.domain.model import (
    uuid_identifier,
)


if TYPE_CHECKING:
    from dataclasses import dataclass  # noqa
else:
    from pydantic.dataclasses import dataclass  # noqa


class DeadLetterNotFound(Exception):  # noqa: N818
    """Необработанное сообщение не найдено."""

    def __init__(self, *args) -> None:
        super().__init__('Необработанное сообщение не найдено', *args)


@dataclass(frozen=True)
class Attempt:
    """Попытка обработки сообщения."""

    failed_at: datetime
    error_message: str
    traceback: str


@dataclass
class DeadLetter:
    """Недоставленное/необработанное сообщение."""

    id: uuid.UUID = uuid_identifier()
    raw_message_value: bytes = Field(title='Содержимое сообщения')
    raw_message_key: Union[bytes, None] = Field(title='Ключ сообщения', default=None)
    topic: str = Field(title='Топик сообщения', max_length=256)
    attempts: tuple[Attempt, ...] = Field(default_factory=tuple, title='Попытки обработки сообщения')
    processed_at: Optional[datetime] = Field(default=None, title='Время успешной обработки сообщения')

    @validator('attempts', always=True)
    @classmethod
    def _validate_attempts(cls, value):
        if not value:
            raise ValueError('Должна быть хотя бы одна попытка обработки')

        return value

    def register_attempt(self, attempt: Attempt) -> None:
        """Добавить информацию о новой попытке обработки."""
        self.attempts = (*self.attempts, attempt)

    def mark_as_processed(self) -> None:
        """Отметить сообщение как успешно обработанное."""
        self.processed_at = datetime.now(tz=timezone.utc)
