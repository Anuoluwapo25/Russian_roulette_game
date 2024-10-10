# import os
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# # Bot command handlers
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Welcome to the Telegram bot! Type /help for available commands.")

# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Available commands:\n/start - Start the bot\n/help - Show this help message")

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(f"You said: {update.message.text}")

# def main():
#     token = os.environ.get('TELEGRAM_BOT_TOKEN')
#     if not token:
#         raise ValueError("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")

#     application = Application.builder().token(token).build()

#     # Add commands
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CommandHandler("help", help_command))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


#     print("Starting bot...")
#     application.run_polling(poll_interval=1)

# if __name__ == '__main__':
#     main()


# from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import CommandHandler, ContextTypes, Application
# import os

# application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     web_app = WebAppInfo(url="https://russian-roulette-game.onrender.com/breevs/")
#     await update.message.reply_text(
#         "Welcome! Click the button below to open Breevs.",
#         reply_markup=InlineKeyboardMarkup.from_button(
#             InlineKeyboardButton(text="Open Breevs", web_app=web_app)
#         )
#     )


# application.add_handler(CommandHandler("start", start))
# # application.run_polling(timeout=0)
# application.run_webhook(
#     listen="0.0.0.0",
#     port=int(os.getenv("PORT")),
#     url_path=os.getenv('TELEGRAM_BOT_TOKEN'),  
#     webhook_url=f"https://russian-roulette-game.onrender.com/{os.getenv('TELEGRAM_BOT_TOKEN')}"
# )


import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, Application
import os

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define PORT correctly at the top level
PORT = int(os.environ.get('PORT', 8000))
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
print('TOKEN')
WEBHOOK_URL = f"https://russian-roulette-game.onrender.com/{TOKEN}"

logger.info(f"Starting bot with PORT: {PORT}, TOKEN: {TOKEN[:5]}..., WEBHOOK_URL: {WEBHOOK_URL}")

application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        logger.info(f"Received /start command from user {update.effective_user.id}")
        web_app = WebAppInfo(url="https://russian-roulette-game.onrender.com/breevs/")
        await update.message.reply_text(
            "Welcome! Click the button below to open Breevs.",
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(text="Open Breevs", web_app=web_app)
            )
        )
        logger.info("Successfully sent response to /start command")
    except Exception as e:
        logger.error(f"Error in start command: {str(e)}", exc_info=True)

application.add_handler(CommandHandler("start", start))

def main():
    try:
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=WEBHOOK_URL
        )
        logger.info(f"Started webhook on port {PORT}")
    except Exception as e:
        logger.error(f"Failed to start webhook: {str(e)}", exc_info=True)

if __name__ == '__main__':
    main()