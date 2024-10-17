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
#     web_app = WebAppInfo(url="https://russian-roullette-4taj.vercel.app/")
#     await update.message.reply_text(
#         "Welcome! Click the button below to open Breevs.",
#         reply_markup=InlineKeyboardMarkup.from_button(
#             InlineKeyboardButton(text="Open Breevs", web_app=web_app)
#         )
#     )


# application.add_handler(CommandHandler("start", start))

# # application.run_polling()
# application.run_webhook(
#     listen="0.0.0.0",
#     port=int(os.getenv('PORT', 8443)),
#     url_path=os.getenv('TELEGRAM_BOT_TOKEN'),  
#     webhook_url=f"https://russian-roulette-game.onrender.com/webhook/{os.getenv('TELEGRAM_BOT_TOKEN')}"
# )







import os
import logging
import asyncio
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
if not bot_token:
    logger.error("TELEGRAM_BOT_TOKEN is not set in the environment.")
    exit(1)

application = Application.builder().token(bot_token).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    web_app = WebAppInfo(url="https://russian-roullette-4taj.vercel.app/")
    await update.message.reply_text(
        "Welcome! Click the button below to open Breevs.",
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text="Open Breevs", web_app=web_app)
        )
    )

application.add_handler(CommandHandler("start", start))



async def run_bot():
    logger.info("Starting the bot with webhook...")
    
    await application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path="webhook", 
        webhook_url="https://russian-roulette-game.onrender.com/webhook/"  
    )

if __name__ == "__main__":
    try:
        # Get the current loop or create a new one
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.run_until_complete(run_bot())
        else:
            asyncio.run(run_bot())
    except Exception as e:
        logger.error(f"Error starting bot: {e}")

# import os
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from dotenv import load_dotenv

# load_dotenv()

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Welcome to the Telegram bot! Type /help for available commands.")

# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Available commands:\n/start - Start the bot\n/help - Show this help message")

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(f"You said: {update.message.text}")

# def main():
#     token = os.getenv('TELEGRAM_BOT_TOKEN')
#     if not token:
#         raise ValueError("No token provided. Set the TELEGRAM_BOT_TOKEN environment variable.")
    
#     webhook_url = os.getenv("WEBHOOK_URL", "https://russian-roulette-game.onrender.com/webhook/")
#     print("Webhook URL:", webhook_url) 

#     if not webhook_url:
#         raise ValueError("No webhook URL provided. Set the WEBHOOK_URL environment variable.")
    
#     application = Application.builder().token(token).build()

#     # Add commands
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CommandHandler("help", help_command))
#     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


#     application.run_polling(poll_interval=1)
    
#     # Set webhook
#     # application.run_webhook(
#     #     listen="0.0.0.0",
#     #     port=int(os.getenv("PORT", "8443")),
#     #     url_path=token,
#     #     webhook_url=f"{webhook_url}"
#     # )

# if __name__ == '__main__':
#     main()
