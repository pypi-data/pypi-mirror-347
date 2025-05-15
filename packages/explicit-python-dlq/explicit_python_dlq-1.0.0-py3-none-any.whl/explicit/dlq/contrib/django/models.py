"""Модели DLQ."""

from uuid import (
    uuid4,
)

from django import (
    VERSION as DJANGO_VERSION,
)
from django.db import (
    models,
)

from explicit.dlq.domain.model import (
    DeadLetter as DomainDeadLetter,
)


if DJANGO_VERSION >= (4, 0):
    from django.db.models import JSONField  # pylint: disable=ungrouped-imports
else:
    from django.contrib.postgres.fields import (
        JSONField,
    )


class DeadLetter(models.Model):
    """Недоставленное/необработанное сообщение."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=DomainDeadLetter.id.title)
    raw_message_value = models.BinaryField(verbose_name=DomainDeadLetter.raw_message_value.title)
    raw_message_key = models.BinaryField(verbose_name=DomainDeadLetter.raw_message_key.title, null=True, blank=True)
    topic = models.CharField(verbose_name=DomainDeadLetter.topic.title, max_length=DomainDeadLetter.topic.max_length)
    attempts = JSONField(verbose_name=DomainDeadLetter.attempts.title)
    processed_at = models.DateTimeField(verbose_name=DomainDeadLetter.processed_at.title, null=True, blank=True)

    # служебные поля используемые для фильтрации и сортировки, чтобы не лезть в json
    _first_attempted_at = models.DateTimeField(db_index=True)
    _attempts_count = models.IntegerField(db_index=True)

    class Meta:  # noqa: D106
        verbose_name = 'Необработанное сообщение'
        verbose_name_plural = 'Необработанные сообщения'
        indexes = [models.Index(fields=['_attempts_count', '_first_attempted_at'], name='dlq_attempts_idx')]
        db_table = 'dlq_dead_letter'
