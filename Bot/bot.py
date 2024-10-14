# # import os
# # from telegram import Update
# # from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# # # Bot command handlers
# # async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     await update.message.reply_text("Welcome to the Telegram bot! Type /help for available commands.")

# # async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     await update.message.reply_text("Available commands:\n/start - Start the bot\n/help - Show this help message")

# # async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     await update.message.reply_text(f"You said: {update.message.text}")

# # def main():
# #     token = os.environ.get('TELEGRAM_BOT_TOKEN')
# #     if not token:
# #         raise ValueError("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")

# #     application = Application.builder().token(token).build()

# #     # Add commands
# #     application.add_handler(CommandHandler("start", start))
# #     application.add_handler(CommandHandler("help", help_command))
# #     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# #     print("Starting bot...")
# #     application.run_polling(poll_interval=1)

# # if __name__ == '__main__':
# #     main()


# from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import CommandHandler, ContextTypes, Application
# import os

# application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     web_app = WebAppInfo(url="https://russian-roullette-4taj.vercel.app/")
#     await update.message.reply_text(
#         "Welcome! Click the button below to open Breevs.",
#         reply_markup=InlineKeyboardMarkup.from_button(
#             InlineKeyboardButton(text="Open Breevs", web_app=web_app)
#         )
#     )


# application.add_handler(CommandHandler("start", start))
# application.run_polling(timeout=20)
# application.run_webhook(
#     listen="0.0.0.0",
#     port=int(os.getenv('PORT')),
#     url_path=os.getenv('TELEGRAM_BOT_TOKEN'),  
#     webhook_url=f"https://russian-roulette-game.onrender.com/webhook/{os.getenv('TELEGRAM_BOT_TOKEN')}"
# )



import os
import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_application():
    """Initialize the Telegram bot application."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("Telegram bot token is not set. Please check your .env file.")
        return None
    return Application.builder().token(token).build()

async def start(update: Update, context):
    """Send a welcome message with a button linking to a Web App."""
    web_app = WebAppInfo(url="https://russian-roullette-4taj.vercel.app/")
    await update.message.reply_text(
        "Welcome! Click the button below to open Breevs.",
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text="Open Breevs", web_app=web_app)
        )
    )

def setup_bot():
    """Set up the bot with command handlers."""
    app = get_application()
    if app:
        app.add_handler(CommandHandler("start", start))
    return app

# if __name__ == "__main__":
#     application = setup_bot()
#     if application:
#         # Webhook setup
#         port = int(os.getenv("PORT", 8443))
#         webhook_url = "https://russian-roulette-game.onrender.com/webhook"
        
#         logger.info("Setting up webhook...")
#         application.run_webhook(
#             listen="0.0.0.0",
#             port=port,
#             url_path="webhook",
#             webhook_url=webhook_url
#         )