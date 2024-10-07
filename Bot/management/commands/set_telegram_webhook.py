# from django.core.management.base import BaseCommand
# from django.conf import settings
# import requests, os

# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')


# class Command(BaseCommand):
#     help = 'Sets webhook for telegram bot'
#     TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

#     def handle(self, *args, **kwargs):
#         bot_token = settings.TELEGRAM_BOT_TOKEN
#         url = f'https://api.telegram.org/bot{bot_token}/setWebhook'
#         webhook_url = f'https://your-render-app-url.com/bot/{bot_token}/'
        
#         response = requests.get(url, params={'url': webhook_url})
        
#         if response.status_code == 200 and response.json()['ok']:
#             self.stdout.write(self.style.SUCCESS('Successfully set webhook'))
#         else:
#             self.stdout.write(self.style.ERROR('Failed to set webhook'))

from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Command(BaseCommand):
    help = 'Sets webhook for telegram bot'

    def handle(self, *args, **kwargs):
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        print(bot_token)

        if not bot_token:
            self.stdout.write(self.style.ERROR('TELEGRAM_BOT_TOKEN not found in environment variables'))
            return

        url = f'https://api.telegram.org/bot{bot_token}/setWebhook'
        webhook_url = f'https://russian-roulette-game.onrender.com/bot/{bot_token}/'

        response = requests.get(url, params={'url': webhook_url})

        if response.status_code == 200 and response.json()['ok']:
            self.stdout.write(self.style.SUCCESS('Successfully set webhook'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to set webhook. Response: {response.text}'))