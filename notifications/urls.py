from django.urls import path
from . import views
from .views import test_notification

urlpatterns = [
    path('get-chat-id/', views.get_my_chat_id, name='get_chat_id'),
    path('send-test/', views.send_test_message, name='send_test_message'),
    path('test/', test_notification, name='test_notification'),
]
