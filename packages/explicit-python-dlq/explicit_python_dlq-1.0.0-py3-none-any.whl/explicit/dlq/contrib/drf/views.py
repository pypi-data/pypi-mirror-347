"""Вьюсеты DeadLetterQueue."""

from abc import (
    abstractmethod,
)

from rest_framework import (
    status,
)
from rest_framework.decorators import (
    action,
)
from rest_framework.filters import (
    SearchFilter,
)
from rest_framework.response import (
    Response,
)
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
)

from explicit.django.domain.validation.exceptions import (
    handle_domain_validation_error,
)
from explicit.dlq.contrib.django.models import (
    DeadLetter,
)
from explicit.dlq.domain.commands import (
    ProcessDeadLetter,
    UpdateDeadLetterRawMessage,
)
from explicit.messagebus.commands import (
    Command,
)

from .serializers import (
    DeadLetterSerializer,
)


class BaseDeadLetterQueueViewSet(ReadOnlyModelViewSet):
    """Необработанные сообщения."""

    queryset = DeadLetter.objects.order_by('_first_attempted_at')
    serializer_class = DeadLetterSerializer
    filter_backends = (SearchFilter,)

    @abstractmethod
    def bus_handle(self, command: Command):
        """Обработчик команды."""

    @action(detail=True, methods=['post'])
    @handle_domain_validation_error
    def process(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Вызвать обработку сообщения."""
        command = ProcessDeadLetter(id=kwargs.get(self.lookup_field))

        self.bus_handle(command)

        return Response(data=self.get_serializer(self.get_object()).data, status=status.HTTP_200_OK)

    @handle_domain_validation_error
    def partial_update(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Обновить данные сообщения."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        command = UpdateDeadLetterRawMessage(id=kwargs.get(self.lookup_field), **serializer.validated_data)

        self.bus_handle(command)

        return Response(data=self.get_serializer(self.get_object()).data, status=status.HTTP_200_OK)
