from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from telegram import Update
from telegram.ext import Application
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from .models import TelegramUser, Player
from rest_framework import status
import os
import os.path
import json
import logging




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
@permission_classes([AllowAny])  
@csrf_exempt
@require_POST
def create_telegram_user(request):
    try:
        data = json.loads(request.body)
        
        # Basic validation
        required_fields = ['telegram_id', 'telegram_username', 'first_name']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }, status=400)
        
        if not data['telegram_id'].isdigit():
            return JsonResponse({
                'success': False,
                'message': 'telegram_id must be numeric'
            }, status=400)
        
        user, created = TelegramUser.objects.update_or_create(
            telegram_id=data['telegram_id'],
            defaults={
                'telegram_username': data['telegram_username'],
                'first_name': data['first_name'],
                'last_name': data.get('last_name', ''),
                'photo_url': data.get('photo_url', ''),
                'username': data['telegram_username'],
            }
        )
        return JsonResponse({
            'success': True,
            'message': 'User created' if created else 'User updated',
            'user_id': user.id
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON in request body'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)

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













