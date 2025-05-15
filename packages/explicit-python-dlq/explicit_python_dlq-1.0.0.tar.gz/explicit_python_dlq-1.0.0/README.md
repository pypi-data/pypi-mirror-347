# Набор компонентов реализующих очередь необработанных сообщений (Dead Letter Queue).

## Пример подключения
testapp/dlq/apps.py:
```python
from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = __package__

    def ready(self):
        self._configure_dlq()

    def _configure_dlq(self):
        from testapp.core import bus
        from explicit.dlq.config import DLQConfig, configure_dlq
        # реализация репозитория специфичная для используемого слоя хранения данных
        from testapp.dlq.adapters.db import Repository
        
        # реализация обработчика сообщений, специфичного для приложения
        from testapp.dlq.services.dispatch import dispatch_message

        config = DLQConfig(
            bus=bus,
            repository=Repository(),
            message_dispatcher=dispatch_message
        )
        # регистрация репозитория и регистрация обработчиков команд
        configure_dlq(config)
```

testapp/dlq/services/dispatch.py:
```python
import json
from explicit.contrib.messagebus.event_registry import Message

from testapp.core import bus
from testapp.core import event_registry

def dispatch_message(raw_message_value: bytes, topic: str):
    """Преобразует сообщение в событие и отправляет его в шину."""
    message = json.loads(raw_message_value)

    if event := event_registry.resolve(
        Message(
            topic=topic,
            type=message.get('type'),
            body=message
        )
    ):
        bus.handle(event)

````

testapp/entrypoints/kafka.py:

```python
def bootstrap() -> None:
    from explicit.dlq.infrastructure.handlers import RegisterInDLQOnFailure

    from testapp.core import bus

    from testapp.dlq.services.dispatch import dispatch_message
    topics = ('test.foo.topic',)

    for raw_message in adapter.subscribe(*topics):
        with RegisterInDLQOnFailure(
            bus=bus,
            topic=raw_message.topic(),
            raw_message_value=raw_message.value(),
            raw_message_key=raw_message.key
        ):
            dispatch_message(raw_message.value(), raw_message.topic())
```
## Готовые компоненты (contrib)

В пакете реализованы готовые к использованию компоненты:
* Реализация абстрактного [хранилища сообщений](./src/explicit/dlq/contrib/django/README.md) на базе Django ORM
* [REST API](./src/explicit/dlq/contrib/drf/README.md) для работы с хранилищем сообщений. Предназначен для совместной работы с реализацией хранилища сообщений django ORM.
