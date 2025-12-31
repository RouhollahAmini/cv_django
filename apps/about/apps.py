from django.apps import AppConfig


class AboutConfig(AppConfig):
    """
    About App Configuration
    این app مربوط به صفحه درباره من و اطلاعات شخصی است
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.about'
    verbose_name = 'درباره من'