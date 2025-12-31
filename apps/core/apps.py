from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Core App Configuration
    این app شامل مدلها و توابع مشترک بین تمام appها است
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = 'Core'