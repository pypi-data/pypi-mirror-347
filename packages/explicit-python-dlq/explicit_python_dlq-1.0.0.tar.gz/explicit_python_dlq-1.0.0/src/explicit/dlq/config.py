"""Конфигурация DLQ."""

from dataclasses import (
    dataclass,
)
from typing import (
    TYPE_CHECKING,
)

from pydantic import (
    ConfigDict,
)

from explicit.dlq.domain import (
    commands,
)
from explicit.dlq.services.handlers import (
    DLQHandlers,
)


if TYPE_CHECKING:
    from explicit.dlq.adapters.db import (
        AbstractDLQRepository,
    )
    from explicit.dlq.types import (
        DLQMessageDispatcher,
    )
    from explicit.messagebus import (
        MessageBus,
    )


@dataclass
class DLQConfig:
    """Конфигурация DLQ."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    bus: 'MessageBus'
    repository: 'AbstractDLQRepository'
    message_dispatcher: 'DLQMessageDispatcher'


def configure_dlq(config: DLQConfig):
    """Настроить DLQ."""
    config.bus.get_uow().register_repositories(('dead_letters', config.repository))

    handlers = DLQHandlers(bus=config.bus, message_dispatcher=config.message_dispatcher)

    config.bus.add_command_handler(
        commands.RegisterDeadLetter,
        handlers.register_dead_letter,  # type: ignore[attr-defined,arg-type]
    )
    config.bus.add_command_handler(
        commands.ProcessDeadLetter,
        handlers.process_dead_letter,  # type: ignore[attr-defined,arg-type]
    )

    config.bus.add_command_handler(
        commands.UpdateDeadLetterRawMessage,
        handlers.update_raw_message_value,  # type: ignore[attr-defined,arg-type]
    )
