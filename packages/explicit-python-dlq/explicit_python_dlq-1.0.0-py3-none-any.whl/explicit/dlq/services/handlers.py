"""Обработчики команд DQL."""

from typing import (
    TYPE_CHECKING,
)

from explicit.dlq.domain import (
    commands,
    factories,
    model,
    services,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
    init_messages_dict,
)


if TYPE_CHECKING:
    from explicit.dlq import (
        types,
    )
    from explicit.messagebus import (
        MessageBus,
    )
    from explicit.unit_of_work import (
        AbstractUnitOfWork,
    )


class DLQHandlers:
    """Обработчики команд DLQ."""

    __slots__ = ('_bus', '_retry_strategy', '_message_dispatcher')

    _bus: 'MessageBus'
    _message_dispatcher: 'types.DLQMessageDispatcher'

    def __init__(
        self,
        bus: 'MessageBus',
        message_dispatcher: 'types.DLQMessageDispatcher',
    ):
        self._bus = bus
        self._message_dispatcher = message_dispatcher

    def register_dead_letter(self, command: commands.RegisterDeadLetter, uow: 'AbstractUnitOfWork') -> model.DeadLetter:
        """Зарегистрировать сообщение, которое не удалось обработать."""
        with uow.wrap():
            return services.register_dead_letter(
                raw_message_value=command.raw_message_value,
                topic=command.topic,
                raw_message_key=command.raw_message_key,
                exception=command.exception,
                uow=uow,
            )

    def process_dead_letter(self, command: commands.ProcessDeadLetter, uow: 'AbstractUnitOfWork') -> model.DeadLetter:
        """Выполнить обработку сообщения."""
        with uow.wrap():
            errors = init_messages_dict()

            data = factories.DeadLetterDTO(id=command.id)
            try:
                dead_letter = uow.dead_letters.get_object_by_id(data.id)  # type: ignore[attr-defined]
            except model.DeadLetterNotFound as dlnf:
                errors['id'].append(str(dlnf))

            if errors:
                raise DomainValidationError(errors)

            try:
                self._message_dispatcher(dead_letter.raw_message_value, dead_letter.topic)
            except Exception as e:  # pylint: disable=broad-exception-caught
                # регистрируем неудачную попытку обработки
                result = services.register_attempt(
                    data=data,
                    exception=e,
                    uow=uow,
                )
            else:
                # регистрируем успешную обработку
                result = services.mark_as_processed(factories.DeadLetterDTO(id=dead_letter.id), uow)

            return result

    def update_raw_message_value(
        self, command: commands.UpdateDeadLetterRawMessage, uow: 'AbstractUnitOfWork'
    ) -> model.DeadLetter:
        """Редактировать содержимое сообщения в DLQ."""
        with uow.wrap():
            data = factories.DeadLetterDTO(id=command.id, raw_message_value=command.raw_message_value)
            dead_letter = services.update_raw_message(data=data, uow=uow)

            return dead_letter
