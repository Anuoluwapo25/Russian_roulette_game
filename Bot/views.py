from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from .bot import bot_updater

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        update = Update.de_json(request.body.decode('utf-8'), bot_updater.bot)
        bot_updater.dispatcher.process_update(update)
    return HttpResponse("OK")