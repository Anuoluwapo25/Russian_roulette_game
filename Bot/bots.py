from telegram import *
from telegram.ext import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from decouple import config
import json


TOKEN = config('TELEGRAM_BOT_TOKEN')
bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dp = updater.dispatcher


@csrf_exempt
def webhook(request):
    print('this is webhook')
    if request.method == 'POST':
        update = Update.de_json(json.loads(request.body), bot)
        dp.process_update(update)

    return HttpResponse('ok')


def start(update: Update, context: CallbackContext) -> None:
    print('this is start')
    update.message.reply_text('Hello World!')


def echo(update: Update, context: CallbackContext) -> None:
    print('this is echo')
    update.message.reply_text(update.message.text)


dp.add_handler(CommandHandler('start', start))

dp.add_handler(MessageHandler(Filters.text, echo))

if __name__ == '__main__':
  print('this is main')

  updater.start_webhook(
    listen="0.0.0.0",
    port=8443,
)

updater.idle()