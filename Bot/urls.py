from django.urls import path
from .views import webhook_view, TelegramUserView, select_number_view

urlpatterns = [
    path('webhook/', webhook_view, name='webhook'),
    # path('webhook', TelegramWebhookView.as_view(), name='telegram_webhook'),
    path('telegram-auth/', TelegramUserView.as_view(), name='telegram_auth'),
    path('select-number/', select_number_view, name='select-number'),
]
