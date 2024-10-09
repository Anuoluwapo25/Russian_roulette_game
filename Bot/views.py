# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
# from telegram import Update
# from telegram.ext import Application
# import json
# import os
# from .bot import application

# @csrf_exempt
# def webhook(request):
#     if request.method == 'POST':
#         token = request.META.get('HTTP_X_TELEGRAM_BOT_API_SECRET_TOKEN')
#         if token != os.environ.get('TELEGRAM_BOT_TOKEN'):
#             return HttpResponse(status=403)

#         try:
#             update = Update.de_json(json.loads(request.body), application.bot)
            
#             application.update_queue.put(update)
            
#             return HttpResponse('OK')
#         except Exception as e:
#             print(f"Error processing update: {str(e)}")
#             return HttpResponse(status=500)
#     else:
#         return HttpResponse(status=405)  

# def set_webhook(request):
#     if request.method == 'GET':
#         bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
#         base_url = getattr(settings, 'TELEGRAM_WEBHOOK_BASE_URL', 'https://your-render-domain.onrender.com')
#         webhook_path = getattr(settings, 'TELEGRAM_WEBHOOK_PATH', f'/bot/webhook/{bot_token}/')
#         webhook_url = f'{base_url}{webhook_path}'

#         try:
#             application.bot.set_webhook(url=webhook_url)
#             return HttpResponse(f"Webhook set to {webhook_url}")
#         except Exception as e:
#             return HttpResponse(f"Failed to set webhook: {str(e)}", status=500)
#     else:
#         return HttpResponse(status=405)  


from django.shortcuts import render

def breevs(request):
    return render(request, 'breevs.html')

