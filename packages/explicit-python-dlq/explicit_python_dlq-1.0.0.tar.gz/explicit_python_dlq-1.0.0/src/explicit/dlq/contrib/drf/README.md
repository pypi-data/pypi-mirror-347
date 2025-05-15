# Реализация REST эндпоинтов DLQ.

## Пример подключения
testapp/rest/dlq/views.py:
```python
from explicit.dlq.contrib.drf.views import BaseDeadLetterQueueViewSet


class DeadLetterQueueViewSet(BaseDeadLetterQueueViewSet):
    """Необработанные сообщения."""

    def bus_handle(self, command):
        """Обработчик команды."""
        from testapp import core

        return core.bus.handle(command)

```

testapp/rest/urls.py:
```python
from rest_framework.routers import SimpleRouter

from testapp.rest.dlq.views import DeadLetterQueueViewSet


router = SimpleRouter()

router.register('dlq', DeadLetterQueueViewSet, basename='dlq')

urlpatterns = router.urls
````
