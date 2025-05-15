## Набор компонентов для интеграции explicit.dlq с Django.
Содержит реализацию репозитория необработанных сообщений.

## Пример подключения
testapp/settings.py:
```python
INSTALLED_APPS = [
    # другие приложения
    'explicit.dlq.contrib.django',  # подключение приложения с моделью DeadLetter
    'testapp.core',                 # настройка компонентов из explicit.dlq
]
```

testapp/dlq/apps.py:
```python

from datetime import timedelta

from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = __package__

    def ready(self):
        self._configure_dlq()

    def _configure_dlq(self):
        from explicit.dlq.config import DLQConfig, configure_dlq
        
        # реализация репозитория на базе Django ORM 
        from explicit.dlq.contrib.django.adapters.db import Repository
        config = DLQConfig(
            # ...
            repository=Repository(),
            # ...
        )
        # регистрация репозитория и регистрация обработчиков команд
        configure_dlq(config)
```
