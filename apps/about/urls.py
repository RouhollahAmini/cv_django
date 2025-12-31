from django.urls import path
from . import views

# نام app برای استفاده در template ها
app_name = 'about'

urlpatterns = [
    # صفحه اصلی درباره من
    # مثال: /about/ یا /
    path('', views.AboutView.as_view(), name='index'),
]