# from django.core.management.base import BaseCommand
# from django.conf import settings
# import requests
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# class Command(BaseCommand):
#     help = 'Sets webhook for Telegram bot'

#     def handle(self, *args, **kwargs):
#         bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')

#         if not bot_token:
#             self.stdout.write(self.style.ERROR('TELEGRAM_BOT_TOKEN not found in environment variables'))
#             return

#         url = f'https://api.telegram.org/bot{bot_token}/setWebhook'
#         webhook_url = f'https://russian-roulette-game.onrender.com/webhook/{bot_token}/'

#         self.stdout.write(self.style.WARNING(f'Setting webhook to: {webhook_url}'))

#         response = requests.get(url, params={'url': webhook_url})

#         if response.status_code == 200 and response.json()['ok']:
#             self.stdout.write(self.style.SUCCESS('Successfully set webhook'))
#         else:
#             self.stdout.write(self.style.ERROR(f'Failed to set webhook. Response: {response.text}'))



# management/commands/setup_webhook.py
from django.core.management.base import BaseCommand
from telegram.ext import Application
from dotenv import load_dotenv
import os

load_dotenv()

class Command(BaseCommand):
    help = 'Sets up the Telegram webhook'

    def handle(self, *args, **options):
        app = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
        webhook_url = f"{os.getenv('WEBHOOK_URL')}/webhook/"
        app.bot.set_webhook(webhook_url)
        self.stdout.write(self.style.SUCCESS(f'Successfully set webhook to {webhook_url}'))