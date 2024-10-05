from telegram import Update
from telegram.ext import Application, CommandHandler
from django.conf import settings
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from models import CustomUser
import logging


User = get_user_model()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define asynchronous start function
async def start(update: Update, context) -> None:
    telegram_user = update.effective_user

    if telegram_user:
        # Use sync_to_async for database operations
        try:
            django_user, created = await sync_to_async(CustomUser.objects.get_or_create)(
                telegram_id=telegram_user.id
            )
            django_user.telegram_username = telegram_user.username
            await sync_to_async(django_user.save)()  # Save the user asynchronously
            
            await update.message.reply_text(f"Hi {telegram_user.first_name}, welcome to the Russian Roulette Game!")
        
        except IntegrityError as e:
            await update.message.reply_text("Error occurred while saving user data.")
            logger.error(f"Database error: {e}")
    
    else:
        await update.message.reply_text("Unable to identify you. Please start the conversation again.")



# from telegram import Update
# from telegram.ext import CallbackContext
# from django.utils import timezone
# from .models import Player, CustomUser  # Or User if you're not using a custom model
# import random

# async def start(update: Update, context: CallbackContext) -> None:
#     telegram_user = update.effective_user
    
#     if telegram_user:
#         try:
#             player = Player.objects.create()
#             custom_user, created = CustomUser.objects.get_or_create(
#                 telegram_id=telegram_user.id,
#                 defaults={
#                     'username': str(telegram_user.id),
#                     'telegram_username': telegram_user.username,
#                     'player': player
#                 }
#             )
#             if not created:
#                 custom_user.telegram_username = telegram_user.username
#                 if not custom_user.player:
#                     custom_user.player = player
#                 custom_user.save()
            
#             await update.message.reply_html(
#                 f"Hi {telegram_user.mention_html()}! Welcome to the Shooting Game. Use /shoot to fire!"
#             )
#         except Exception as e:
#             print(f"Error in start function: {e}")
#             await update.message.reply_text("An error occurred. Please try again later.")
#     else:
#         await update.message.reply_text("Unable to identify you. Please start the conversation again.")


# async def shoot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     user = update.effective_user
#     try:
#         custom_user = CustomUser.objects.get(telegram_id=user.id)
#         player = custom_user.player
        
#         if player is None:
#             player = Player.objects.create()
#             custom_user.player = player
#             custom_user.save()

#         current_time = timezone.now()
#         if player.last_shot_time and (current_time - player.last_shot_time).seconds < 5:
#             await update.message.reply_text("You need to wait 5 seconds between shots!")
#             return
        
#         if random.random() < 0.5:
#             player.score += 1
#             player.save()
#             await update.message.reply_text(f"Hit! Your score is now {player.score}")
#         else:
#             await update.message.reply_text("Miss! Try again.")
        
#         player.last_shot_time = current_time
#         player.save()
#     except CustomUser.DoesNotExist:
#         await update.message.reply_text("You need to start the game first. Use /start command.")
#     except Exception as e:
#         print(f"Error in shoot function: {e}")
#         await update.message.reply_text("An error occurred. Please try again.")