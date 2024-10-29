# from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# from telegram.ext import CommandHandler, ContextTypes, Application, ApplicationBuilder
# import os
# import logging

# # Setup logging for better monitoring of the bot
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     level=logging.INFO
# )

# # Ensure required environment variables are present
# TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# WEBHOOK_URL = f"https://russian-roulette-game.onrender.com/webhook/{TELEGRAM_TOKEN}"
# PORT = int(os.getenv("PORT", 8443))

# if not TELEGRAM_TOKEN:
#     raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables.")

# # Initialize application with the bot token
# application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# # Define the /start command handler
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
#         web_app = WebAppInfo(url="https://russian-roullette-4taj.vercel.app/")
#         await update.message.reply_text(
#             "Welcome! Click the button below to open Breevs.",
#             reply_markup=InlineKeyboardMarkup.from_button(
#                 InlineKeyboardButton(text="Open Breevs", web_app=web_app)
#             )
#         )
#     except Exception as e:
#         logging.error(f"Error in /start handler: {e}")
#         await update.message.reply_text("Something went wrong. Please try again later.")

# # Add the command handler to the application
# application.add_handler(CommandHandler("start", start))

# # application.run_polling()

# if __name__ == '__main__':
#     print('this is main')

#     app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

#     app.add_handler(CommandHandler('start', start))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

#     # Start the webhook
#     app.run_webhook(
#         listen="0.0.0.0",
#         port=8443,
#         url_path=TELEGRAM_TOKEN,  # Set your webhook URL path
#         webhook_url=f"https://<your-domain.com>/{TELEGRAM_TOKEN}"  # Replace with your actual domain
#     )


# def main():
#     try:
#         logging.info("Starting bot with webhook...")
#         application.run_webhook(
#             listen="0.0.0.0",
#             port=PORT,
#             url_path=TELEGRAM_TOKEN,  # This secures the webhook endpoint
#             webhook_url=WEBHOOK_URL
#         )
#     except Exception as e:
#         logging.error(f"Error while running webhook: {e}")
#         raise

# if __name__ == "__main__":
    # main()





import os
import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = f"https://russian-roulette-game.onrender.com/webhook/{TELEGRAM_TOKEN}"
PORT = int(os.getenv("PORT", 8443))

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set in environment variables.")


application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        web_app = WebAppInfo(url="https://russian-roullette-4taj.vercel.app/")
        await update.message.reply_text(
            "Welcome! Click the button below to open Breevs.",
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(text="Open Breevs", web_app=web_app)
            )
        )
    except Exception as e:
        logging.error(f"Error in /start handler: {e}")
        await update.message.reply_text("Something went wrong. Please try again later.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('this is echo')
    try:
        echoed_message = update.message.text
        web_app = WebAppInfo(url="https://russian-roullette-4taj.vercel.app/")
        
        await update.message.reply_text(
            f"You said: {echoed_message}. Click the button below to open Breevs.",
            reply_markup=InlineKeyboardMarkup.from_button(
                InlineKeyboardButton(text="Open Breevs", web_app=web_app)
            )
        )
    except Exception as e:
        logging.error(f"Error in echo handler: {e}")
        await update.message.reply_text("Something went wrong. Please try again later.")


application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

if __name__ == '__main__':
    print('Starting the bot...')

  
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_TOKEN,  
        webhook_url='https://russian-roulette-game.onrender.com/' 
    )
