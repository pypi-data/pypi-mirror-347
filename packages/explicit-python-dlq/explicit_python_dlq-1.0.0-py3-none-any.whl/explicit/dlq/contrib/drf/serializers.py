"""Сериализаторы для работы DeadLetter."""

# pylint: disable=abstract-method
from rest_framework import (
    serializers,
)

from explicit.dlq.contrib.django.models import (
    DeadLetter,
)


class _AttemptSerializer(serializers.Serializer):
    """Сериализатор попытки обработки сообщения."""

    failed_at = serializers.DateTimeField(label='Время неудачной попытки')
    error_message = serializers.CharField(label='Сообщение об ошибке')
    traceback = serializers.CharField()


class DeadLetterSerializer(serializers.ModelSerializer):
    """Сериализатор необработанного сообщения."""

    raw_message_value = serializers.CharField(allow_blank=False)
    raw_message_key = serializers.CharField(allow_blank=True, allow_null=True, read_only=True)
    attempts = _AttemptSerializer(many=True, read_only=True)

    def to_internal_value(self, data):  # noqa: D102
        ret = super().to_internal_value(data)
        ret['raw_message_value'] = ret['raw_message_value'].encode()
        if ret.get('raw_message_key'):
            ret['raw_message_key'] = ret['raw_message_key'].encode()
        return ret

    def to_representation(self, instance):  # noqa: D102
        ret = super().to_representation(instance)
        ret['raw_message_value'] = bytes(instance.raw_message_value).decode()
        if instance.raw_message_key:
            ret['raw_message_key'] = bytes(instance.raw_message_key).decode()
        return ret

    class Meta:  # noqa: D106
        model = DeadLetter
        read_only_fields = ('id', 'raw_message_key', 'topic', 'attempts', 'processed_at')
        exclude = ('_first_attempted_at', '_attempts_count')
