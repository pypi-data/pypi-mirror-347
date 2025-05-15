"""Адаптеры для работы с Dead Letter Queue (DLQ) в базе данных."""

from typing import (
    TYPE_CHECKING,
    Iterator,
    Union,
)

from django.core.exceptions import (
    ObjectDoesNotExist,
)

from explicit.dlq.adapters.db import (
    AbstractDLQRepository,
)
from explicit.dlq.domain.model import (
    DeadLetter,
    DeadLetterNotFound,
)
from explicit.domain import (
    asdict,
)


if TYPE_CHECKING:
    from uuid import (
        UUID,
    )

    from explicit.dlq.contrib.django import (
        models as db,
    )


class Repository(AbstractDLQRepository):
    """Репозиторий DeadLetterQueue."""

    @property
    def _base_qs(self):
        # pylint: disable-next=import-outside-toplevel
        from explicit.dlq.contrib.django.models import (
            DeadLetter as DBDeadLetter,
        )

        return DBDeadLetter.objects.order_by('_first_attempted_at')

    def _to_domain(self, dbinstance: 'db.DeadLetter') -> DeadLetter:
        return DeadLetter(
            id=dbinstance.id,
            raw_message_value=bytes(dbinstance.raw_message_value),
            raw_message_key=bytes(dbinstance.raw_message_key) if dbinstance.raw_message_key else None,
            topic=dbinstance.topic,
            attempts=tuple(dbinstance.attempts),
            processed_at=dbinstance.processed_at,
        )

    def _to_db(self, modelinstance: DeadLetter) -> DeadLetter:
        # pylint: disable-next=import-outside-toplevel
        from explicit.dlq.contrib.django.models import (
            DeadLetter as DBDeadLetter,
        )

        assert isinstance(modelinstance, DeadLetter)
        db_instance, _ = DBDeadLetter.objects.update_or_create(
            pk=modelinstance.id,
            defaults=asdict(modelinstance, exclude={'id', 'attempts'})
            | {
                'attempts': [
                    asdict(attempt) | {'failed_at': attempt.failed_at.isoformat()} for attempt in modelinstance.attempts
                ],
                '_first_attempted_at': modelinstance.attempts[0].failed_at,
                '_attempts_count': len(modelinstance.attempts),
            },
        )
        return self.get_object_by_id(db_instance.pk)

    def add(self, obj: DeadLetter) -> DeadLetter:
        """Добавить сообщение."""
        return self._to_db(obj)

    def update(self, obj: DeadLetter) -> DeadLetter:
        """Обновить сообщение."""
        assert isinstance(obj, DeadLetter)

        return self._to_db(obj)

    def delete(self, obj: DeadLetter) -> None:
        """Удалить сообщение."""
        assert isinstance(obj, DeadLetter)

        self._base_qs.filter(pk=obj.id).delete()

    def get_all_objects(self) -> Iterator[DeadLetter]:
        """Получить все сообщения."""
        for db_instance in self._base_qs.iterator():
            yield self._to_domain(db_instance)

    def get_object_by_id(self, identifier: 'Union[UUID, str]') -> DeadLetter:
        """Получить сообщение по идентификатору."""
        try:
            db_instance = self._base_qs.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as exc:
            raise DeadLetterNotFound from exc
