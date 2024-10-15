# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.utils.decorators import method_decorator
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import api_view, permission_classes
# from telegram import Update
# from telegram.ext import ApplicationBuilder
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework import status
# import os
# import json

# # Telegram bot setup
# application = ApplicationBuilder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

# class TelegramWebhookView(APIView):
#     def post(self, request):
#         try:
#             update = Update.de_json(json.loads(request.body), application.bot)
#             application.process_update(update)
#             return Response({"status": "ok"})
#         except json.JSONDecodeError:
#             return Response({"error": "Invalid JSON"}, status=400)
        
#     # return Response({"error": "Invalid request"}, status=400)


# @method_decorator(csrf_exempt, name='dispatch')
# class TelegramAuthView(APIView):
#     def post(self, request):
#         try:
#             telegram_data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(request, telegram_data=telegram_data)

#         if user is not None:
#             login(request, user)
#             return Response({
#                 'id': user.id,
#                 'telegram_id': user.telegram_id,
#                 'username': user.username,
#                 'first_name': user.first_name,
#                 'last_name': user.last_name,
#                 'photo_url': user.photo_url,
#                 'auth_date': user.auth_date.isoformat(),
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)



# class GetUserView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         return Response({
#             'id': user.id,
#             'telegram_id': user.telegram_id,
#             'username': user.username,
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'photo_url': user.photo_url,
#             'auth_date': user.auth_date.isoformat(),
#         })


# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from .bot import setup_bot, get_application
# from telegram import Update

# bot = setup_bot()

# @csrf_exempt
# def telegram_webhook(request):
#     if request.method == 'POST':
#         update = Update.de_json(request.body.decode('utf-8'), get_application().bot)
#         bot.process_update(update)
#     return HttpResponse()


import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram.ext import Application
from telegram import Update
from .bot import application
import logging

logger = logging.getLogger(__name__)

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")  
application = Application.builder().token(bot_token).build()

@csrf_exempt  
def webhook_view(request):
    if request.method == "POST":
        try:
            update_data = json.loads(request.body)
            logger.debug(f"Raw request body: {update_data}")
            update = Update.de_json(update_data, application.bot)
            # Process the update asynchronously
            application.update_queue.put_nowait(update)
            return JsonResponse({"status": "ok"}, status=200)
        except Exception as e:
            print(f"Error handling webhook request: {e}")
            return JsonResponse({"status": "error", "error": str(e)}, status=500)
    return JsonResponse({"status": "not allowed"}, status=405)











