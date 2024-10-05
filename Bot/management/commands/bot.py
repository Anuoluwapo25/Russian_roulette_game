# from django.core.management.base import BaseCommand
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler
# from django.utils import timezone
# from Bot.models import CustomUser, Player  # Import your models
# import random
# import logging

# # Set up logging
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# class Command(BaseCommand):
#     help = 'Runs the Telegram bot'

#     def handle(self, *args, **kwargs):
#         TOKEN = '7618149231:AAEexKMU147voLpVvfbTc_av4ZRMsShiYQ4'

#         def start(update: Update, context):
#             telegram_user = update.effective_user

#             if telegram_user:
#                 # Get or create CustomUser based on the telegram_id
#                 django_user, created = CustomUser.objects.get_or_create(
#                     telegram_id=telegram_user.id,
#                     defaults={'username': telegram_user.username}
#                 )

#                 # Update Telegram username if necessary
#                 if created or django_user.telegram_username != telegram_user.username:
#                     django_user.telegram_username = telegram_user.username
#                     django_user.save()

#                 # Create or retrieve the player associated with the CustomUser
#                 player, _ = Player.objects.get_or_create(user=django_user)

#                 update.message.reply_html(
#                     f"Hi {telegram_user.mention_html()}! Welcome to the Shooting Game. Use /shoot to fire!"
#                 )
#             else:
#                 update.message.reply_text("Unable to identify you. Please start the conversation again.")

#         def shoot(update: Update, context):
#             telegram_user = update.effective_user
#             django_user = CustomUser.objects.get(telegram_id=telegram_user.id)
#             player, _ = Player.objects.get_or_create(user=django_user)

#             current_time = timezone.now()
#             if hasattr(player, 'last_shot_time') and (current_time - player.last_shot_time).seconds < 5:
#                 update.message.reply_text("You need to wait 5 seconds between shots!")
#                 return

#             if random.random() < 0.5:
#                 player.score += 1
#                 player.save()
#                 update.message.reply_text(f"Hit! Your score is now {player.score}")
#             else:
#                 update.message.reply_text("Miss! Try again.")

#             player.last_shot_time = current_time
#             player.save()

#         def unknown(update: Update, context):
#             """Handles unknown commands"""
#             update.message.reply_text("Sorry, I didn't understand that command.")

#         # Create bot application and set up handlers
#         application = Application.builder().token(TOKEN).build()

#         # Register handlers for commands and messages
#         application.add_handler(CommandHandler("start", start))
#         application.add_handler(CommandHandler("shoot", shoot))
#         # application.add_handler(MessageHandler(Filters.command, unknown))

#         # Start the bot (polling for updates)
#         application.run_polling()


# from asgiref.sync import sync_to_async
# from django.core.management.base import BaseCommand
# from Bot.models import CustomUser, Player
# from telegram import Update
# from telegram.ext import Application, CommandHandler, ContextTypes

# class Command(BaseCommand):
#     help = 'Runs the Telegram bot'

#     @sync_to_async
#     def get_or_create_user(self, telegram_id, username):
#         return CustomUser.objects.get_or_create(
#             telegram_id=telegram_id,
#             defaults={'username': username}
#         )

#     async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#         user = update.effective_user
#         django_user, created = await self.get_or_create_user(user.id, user.username)
        
#         # Rest of your start function...

#     def handle(self, *args, **options):
#         application = Application.builder().token("7618149231:AAEexKMU147voLpVvfbTc_av4ZRMsShiYQ4").build()
#         application.add_handler(CommandHandler("start", self.start))
#         application.run_polling()


# ____

# from django.core.management.base import BaseCommand
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters
# from django.utils import timezone
# from Bot.models import CustomUser, Player
# import random
# import logging
# from asgiref.sync import sync_to_async

# # Set up logging
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# class Command(BaseCommand):
#     help = 'Runs the Telegram bot'

#     @sync_to_async
#     def get_or_create_user(self, telegram_id, username):
#         django_user, created = CustomUser.objects.get_or_create(
#             telegram_id=telegram_id,
#             defaults={'username': username}
#         )
#         if created or django_user.telegram_username != username:
#             django_user.telegram_username = username
#             django_user.save()
#         return django_user

#     @sync_to_async
#     def get_or_create_player(self, django_user):
#         return Player.objects.get_or_create(user=django_user)

#     # @sync_to_async
#     # def update_player_score(self, player, score_increment):
#     #     player.score += score_increment
#     #     player.last_shot_time = timezone.now()
#     #     player.save()
#     #     return player.score

#     async def start(self, update: Update, context):
#         telegram_user = update.effective_user
#         if telegram_user:
#             django_user = await self.get_or_create_user(telegram_user.id, telegram_user.username)
#             await self.get_or_create_player(django_user)
#             await update.message.reply_html(
#                 f"Hi {telegram_user.mention_html()}! Welcome to the Shooting Game. Use /shoot to fire!"
#             )
#         else:
#             await update.message.reply_text("Unable to identify you. Please start the conversation again.")

#     async def shoot(self, update: Update, context):
#         telegram_user = update.effective_user
#         django_user = await self.get_or_create_user(telegram_user.id, telegram_user.username)
#         player, _ = await self.get_or_create_player(django_user)

#         current_time = timezone.now()
#         if hasattr(player, 'last_shot_time') and (current_time - player.last_shot_time).seconds < 5:
#             await update.message.reply_text("You need to wait 5 seconds between shots!")
#             return

#         if random.random() < 0.5:
#             score = await self.update_player_score(player, 1)
#             await update.message.reply_text(f"Hit! Your score is now {score}")
#         else:
#             await self.update_player_score(player, 0)  # Just to update last_shot_time
#             await update.message.reply_text("Miss! Try again.")

#     async def unknown(self, update: Update, context):
#         """Handles unknown commands"""
#         await update.message.reply_text("Sorry, I didn't understand that command.")

#     def handle(self, *args, **kwargs):
#         TOKEN = '7618149231:AAEexKMU147voLpVvfbTc_av4ZRMsShiYQ4'

#         # Create bot application and set up handlers
#         application = Application.builder().token(TOKEN).build()

#         # Register handlers for commands and messages
#         application.add_handler(CommandHandler("start", self.start))
#         application.add_handler(CommandHandler("shoot", self.shoot))
#         application.add_handler(MessageHandler(filters.COMMAND, self.unknown))

#         # Start the bot (polling for updates)
#         application.run_polling()


from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from django.utils import timezone
from Bot.models import CustomUser, Player
import random
import logging
from asgiref.sync import sync_to_async

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    @sync_to_async
    def get_or_create_user(self, telegram_id, username):
        django_user, created = CustomUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={'username': username}
        )
        if created or django_user.telegram_username != username:
            django_user.telegram_username = username
            django_user.save()
        return django_user

    @sync_to_async
    def get_or_create_player(self, django_user):
        return Player.objects.get_or_create(user=django_user)

    # @sync_to_async
    # def update_player_score(self, player, score_increment):
    #     player.score += score_increment
    #     player.last_shot_time = timezone.now()
    #     player.save()
    #     return player.score

    async def start(self, update: Update, context):
        telegram_user = update.effective_user
        if telegram_user:
            django_user = await self.get_or_create_user(telegram_user.id, telegram_user.username)
            await self.get_or_create_player(django_user)
            await update.message.reply_html(
                f"Hi {telegram_user.mention_html()}! Welcome to the Shooting Game. Use /shoot to fire!"
            )
        else:
            await update.message.reply_text("Unable to identify you. Please start the conversation again.")

    async def shoot(self, update: Update, context):
        telegram_user = update.effective_user
        django_user = await self.get_or_create_user(telegram_user.id, telegram_user.username)
        player, _ = await self.get_or_create_player(django_user)

        current_time = timezone.now()
        if hasattr(player, 'last_shot_time') and (current_time - player.last_shot_time).seconds < 5:
            await update.message.reply_text("You need to wait 5 seconds between shots!")
            return

        if random.random() < 0.5:
            score = await self.update_player_score(player, 1)
            await update.message.reply_text(f"Hit! Your score is now {score}")
        else:
            await self.update_player_score(player, 0)  # Just to update last_shot_time
            await update.message.reply_text("Miss! Try again.")

    async def unknown(self, update: Update, context):
        """Handles unknown commands"""
        await update.message.reply_text("Sorry, I didn't understand that command.")

    def handle(self, *args, **kwargs):
        TOKEN = '7618149231:AAEexKMU147voLpVvfbTc_av4ZRMsShiYQ4'

        # Create bot application and set up handlers
        application = Application.builder().token(TOKEN).build()

        # Register handlers for commands and messages
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("shoot", self.shoot))
        application.add_handler(MessageHandler(filters.COMMAND, self.unknown))

        # Start the bot (polling for updates)
        application.run_polling()