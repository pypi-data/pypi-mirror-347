"""Инфраструктурные компоненты DQL."""

from contextlib import (
    AbstractContextManager,
)
from typing import (
    Optional,
)

from explicit.dlq.domain.commands import (
    RegisterDeadLetter,
)
from explicit.messagebus import (
    MessageBus,
)


class RegisterInDLQOnFailure(AbstractContextManager):
    """Контекстный менеджер для обработки ошибок при обработке сообщений.

    Перехватывает исключения при обработке сообщения и регистрирует такие сообщения в DLQ.

    Пример использования:

    .. code-block:: python
        for raw_message_value in adapter.subscribe(*registered_topics):
            with RegisterInDLQOnFailure(
                bus=bus,
                topic=raw_message_value.topic(),
                raw_message_value=raw_message_value.value(),
                raw_message_key=raw_message_value.raw_message_key(),
            ):
                message = json.loads(raw_message_value.value())
                if event := event_registry.resolve(Message(...)):
                    bus.handle(event)
    """

    def __init__(
        self,
        bus: 'MessageBus',
        topic: str,
        raw_message_value: bytes,
        raw_message_key: Optional[bytes] = None,
    ):
        self._bus = bus
        self._topic = topic
        self._raw_message_value = raw_message_value
        self._raw_message_key = raw_message_key

    def __enter__(self):
        """Вход в менеджер контекста."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Зарегистрировать сообщение в DLQ при возникновении исключения."""
        ret = False

        if exc_val is not None:
            command = RegisterDeadLetter(
                topic=self._topic,
                raw_message_value=self._raw_message_value,
                raw_message_key=self._raw_message_key,
                exception=exc_val,
            )
            try:
                self._bus.handle(command)
            except Exception as registration_exc:
                raise registration_exc from exc_val

            ret = True

        return ret
