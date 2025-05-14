from django.apps import AppConfig


class InteractionLoggerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'interaction_logger'
    verbose_name = 'User Activity Logger'
