from django.http import HttpResponse
# from django.shortcuts import render
# from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from telegram import Update
import json
from django.views.decorators.http import require_POST

from .bot import bot_application

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        update = Update.de_json(request.body.decode('utf-8'), bot_application.bot)
        bot_application.process_update(update)
    return HttpResponse("OK")