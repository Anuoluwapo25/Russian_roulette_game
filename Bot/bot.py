from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, Application
import os


application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    web_app = WebAppInfo(url="https://russian-roullette-4taj.vercel.app/")
    await update.message.reply_text(
        "Welcome! Click the button below to open Breevs.",
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text="Open Breevs", web_app=web_app)
        )
    )


application.add_handler(CommandHandler("start", start))

# application.run_polling()
application.run_webhook(
    listen="0.0.0.0",
    port=int(os.getenv('PORT', 8443)),
    url_path=os.getenv('TELEGRAM_BOT_TOKEN'),  
    webhook_url=f"https://russian-roulette-game.onrender.com/webhook/{os.getenv('TELEGRAM_BOT_TOKEN')}"
)







