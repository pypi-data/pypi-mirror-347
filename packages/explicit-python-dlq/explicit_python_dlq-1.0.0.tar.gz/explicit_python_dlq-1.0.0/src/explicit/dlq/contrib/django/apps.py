"""Конфигурация приложения."""

from django.apps import (
    AppConfig as AppConfigBase,
)


class AppConfig(AppConfigBase):
    """Конфигурация приложения."""

    name = __package__
    label = 'explicit_dlq_django'
