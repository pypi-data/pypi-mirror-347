"""DTO и фабрики DLQ."""

import traceback
from datetime import (
    datetime,
    timezone,
)
from typing import (
    Union,
)

from explicit.domain import (
    Str,
    UnsetUUID,
)
from explicit.domain.factories import (
    AbstractDomainFactory,
    DTOBase,
)
from explicit.domain.model import (
    Unset,
    unset,
)
from explicit.domain.types import (
    NoneStr,
)

from .model import (
    Attempt,
    DeadLetter,
)


class AttemptDTO(DTOBase):
    """Объект передачи данных о попытке обработки сообщения."""

    failed_at: Union[datetime, Unset] = unset
    error_message: Str = unset
    traceback: Str = unset


class DeadLetterDTO(DTOBase):
    """Объект передачи данных о необработанном сообщении."""

    id: UnsetUUID = unset
    raw_message_value: Union[bytes, Unset] = unset
    raw_message_key: NoneStr = unset
    topic: Str = unset
    attempts: Union[list[AttemptDTO], Unset] = unset
    processed_at: Union[datetime, None, Unset] = unset


class Factory(AbstractDomainFactory):
    """Фабрика для создания объектов предметной области DLQ."""

    def create(self, data: DeadLetterDTO) -> DeadLetter:
        """Создать DLQ из DTO."""
        params = data.dict()

        return DeadLetter(**params)

    def create_attempt_from_exception(self, exception: Exception) -> Attempt:
        """Создать запись о попытке обработки из исключения."""
        return Attempt(
            failed_at=datetime.now(tz=timezone.utc),
            error_message=str(exception),
            traceback=''.join(traceback.format_exception(type(exception), exception, exception.__traceback__)),
        )

    def create_from_exception(
        self, raw_message_value: bytes, raw_message_key: Union[bytes, None], topic: str, exception: Exception
    ) -> DeadLetter:
        """Создать DLQ из исключения."""
        attempt = self.create_attempt_from_exception(exception)

        return DeadLetter(
            raw_message_value=raw_message_value, raw_message_key=raw_message_key, topic=topic, attempts=(attempt,)
        )


factory = Factory()
