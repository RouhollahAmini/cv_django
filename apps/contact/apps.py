from django.apps import AppConfig


class ContactConfig(AppConfig):
    """
    Contact App Configuration
    این app مربوط به صفحه تماس با من و فرم های تماس است
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contact'
    verbose_name = 'تماس با من'