from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    Blog App Configuration
    این app مربوط به وبلاگ و مقالات است
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blog'
    verbose_name = 'وبلاگ'