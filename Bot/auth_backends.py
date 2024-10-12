import os
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
import hashlib
import hmac
import time


load_dotenv()

User = get_user_model()

class TelegramAuthBackend:
    def authenticate(self, request, telegram_data=None):
        if not telegram_data:
            return None

        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set in the environment")

        # Verify the data
        data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(telegram_data.items()) if k != 'hash')
        secret_key = hashlib.sha256(bot_token.encode()).digest()
        computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if computed_hash != telegram_data['hash']:
            return None

        # Check if the auth date is not older than 1 day
        auth_date = int(telegram_data['auth_date'])
        if time.time() - auth_date > 86400:
            return None

        # Get or create user based on Telegram ID
        user, created = User.objects.update_or_create(
            telegram_id=telegram_data['id'],
            defaults={
                'username': telegram_data.get('username', ''),
                'first_name': telegram_data.get('first_name', ''),
                'last_name': telegram_data.get('last_name', ''),
                'photo_url': telegram_data.get('photo_url', ''),
            }
        )

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None