# pylint: disable=missing-module-docstring,invalid-name
import uuid

from django import (
    VERSION as DJANGO_VERSION,
)
from django.db import (
    migrations,
    models,
)


if DJANGO_VERSION >= (4, 0):
    from django.db.models import (
        JSONField,
    )
else:
    from django.contrib.postgres.fields import (
        JSONField,
    )


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='DeadLetter',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name='Идентификатор UUID',
                    ),
                ),
                ('raw_message_value', models.BinaryField(verbose_name='Содержимое сообщения')),
                ('raw_message_key', models.BinaryField(verbose_name='Ключ сообщения', null=True, blank=True)),
                ('topic', models.CharField(max_length=256, verbose_name='Топик сообщения')),
                ('attempts', JSONField(verbose_name='Попытки обработки сообщения')),
                (
                    'processed_at',
                    models.DateTimeField(blank=True, null=True, verbose_name='Время успешной обработки сообщения'),
                ),
                ('_first_attempted_at', models.DateTimeField(db_index=True)),
                ('_attempts_count', models.IntegerField(db_index=True)),
            ],
            options={
                'verbose_name': 'Необработанное сообщение',
                'verbose_name_plural': 'Необработанные сообщения',
                'indexes': [models.Index(fields=['_attempts_count', '_first_attempted_at'], name='dlq_attempts_idx')],
                'db_table': 'dlq_dead_letter',
            },
        ),
    ]
