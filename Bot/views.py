from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from telegram import Update
from telegram.ext import Application
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import os
import os.path
import json
import logging
from asgiref.sync import async_to_sync
from .models import Player
from .auth_backends import TelegramAuthBackend




logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
application = Application.builder().token(bot_token).build()

@csrf_exempt
def webhook_view(request):
    if request.method == "POST":
        try:
            logger.debug("Received webhook POST request")
            logger.debug(f"Request body: {request.body}")

            update_data = json.loads(request.body)
            logger.info(f"Raw request body: {update_data}")
            
            update = Update.de_json(update_data, application.bot)
            logger.debug(f"Telegram update object: {update}") 
           
            async_to_sync(application.update_queue.put)(update)
            return JsonResponse({"status": "ok"}, status=200)
        except Exception as e:
            logger.error(f"Error handling webhook request: {e}", exc_info=True)
            return JsonResponse({"status": "error", "error": str(e)}, status=500)
    return JsonResponse({"status": "not allowed"}, status=405)


@method_decorator(csrf_exempt, name='dispatch')
class TelegramAuthView(APIView):
    def post(self, request):
        auth_data = request.data
        backend = TelegramAuthBackend()
        user = backend.authenticate(request, telegram_data=auth_data)
        
        if user:
            login(request, user, backend='authentication.TelegramAuthBackend')
            player, created = Player.objects.get_or_create(user=user)
            return Response({
                'message': 'Authentication successful',
                'user_id': user.id,
                'player_id': player.id
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Authentication failed'
            }, status=status.HTTP_401_UNAUTHORIZED)

class GetUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'telegram_id': user.telegram_id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'photo_url': user.photo_url,
            'auth_date': user.auth_date.isoformat(),
        })













