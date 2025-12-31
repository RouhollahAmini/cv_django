from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    # صفحه تماس
    path('', views.ContactView.as_view(), name='contact'),
    
    # ارسال پیام (AJAX)
    path('send-message/', views.SendMessageView.as_view(), name='send_message'),
]