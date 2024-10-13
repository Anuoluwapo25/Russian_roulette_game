from django.urls import path
from .views import TelegramWebhookView

urlpatterns = [
    path('webhook/', TelegramWebhookView.as_view(), name='telegram_webhook'),
    # path('telegram-auth/', TelegramAuthView.as_view(), name='telegram_auth'),
    # path('get-user/', GetUserView.as_view(), name='get_user'),
]
