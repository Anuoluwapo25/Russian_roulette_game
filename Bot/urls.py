from django.urls import path
from .views import webhook_view, TelegramUserView

urlpatterns = [
    path('webhook/', webhook_view, name='webhook'),
    # path('webhook', TelegramWebhookView.as_view(), name='telegram_webhook'),
    path('telegram-auth/', TelegramUserView.as_view(), name='telegram_auth'),
]
