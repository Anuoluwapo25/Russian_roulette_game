from django.urls import path
from . import views

urlpatterns = [
    path('<str:token>/', views.telegram_webhook, name='telegram_webhook'),
]