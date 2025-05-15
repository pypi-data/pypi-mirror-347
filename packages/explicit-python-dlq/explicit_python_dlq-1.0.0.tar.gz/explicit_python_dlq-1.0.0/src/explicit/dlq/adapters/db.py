"""Адаптеры для работы с Dead Letter Queue (DLQ) в базе данных."""

from abc import (
    ABCMeta,
)

from explicit.adapters.db import (
    AbstractRepository,
)


class AbstractDLQRepository(AbstractRepository, metaclass=ABCMeta):
    """Абстрактный репозиторий для работы с DLQ."""
