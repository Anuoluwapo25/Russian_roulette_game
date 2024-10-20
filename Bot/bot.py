import os
import logging
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

# application.run_polling(poll_interval=1)

async def run_bot():
    logger.info("Starting the bot with webhook...")
    
    await application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path="webhook", 
        webhook_url="https://russian-roulette-game.onrender.com/webhook/"  
    )

