from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from telegram import Update
from telegram.ext import Application
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import os
import os.path
import json
import logging
from asgiref.sync import async_to_sync
from .models import TelegramUser




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



# @method_decorator(csrf_exempt, name='dispatch')
# class TelegramUserView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         logger.info("Received POST request to TelegramUserView")
#         logger.debug(f"Request data: {request.data}")
        
#         try:
#             data = request.data
            
#             telegram_id = data.get('id')
#             first_name = data.get('first_name')
#             last_name = data.get('last_name', '')
#             photo_url = data.get('photo_url', None)

#             if not telegram_id:
#                 return Response({
#                     'message': 'telegram_id (id) is required'
#                 }, status=status.HTTP_400_BAD_REQUEST)
            
#             # Check if the user already exists
#             user, created = TelegramUser.objects.update_or_create(
#                 telegram_id=telegram_id,
#                 defaults={
#                     'first_name': first_name,
#                     'last_name': last_name,
#                     'photo_url': photo_url,
#                 }
#             )
            
#             if created:
#                 logger.info(f"Created new user: {user.telegram_id}")
#             else:
#                 logger.info(f"Updated existing user: {user.telegram_id}")
                
#             return Response({
#                 'message': 'Data stored successfully',
#                 'user_id': user.id
#             }, status=status.HTTP_200_OK)
        
#         except Exception as e:
#             logger.error(f"Error while saving data: {str(e)}")
#             return Response({
#                 'message': 'Internal server error',
#                 'error': str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class TelegramUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Received POST request to TelegramUserView")
        logger.info(f"Request data: {request.data}")

        try:
            data = request.data

            telegram_id = str(data.get('id'))  # Convert to string to ensure consistent type
            first_name = data.get('first_name')
            last_name = data.get('last_name', '')
            photo_url = data.get('photo_url', None)
            auth_date = data.get('auth_date')

            if not telegram_id:
                logger.error("Missing telegram_id in request")
                return Response({
                    'message': 'telegram_id (id) is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Log the data we're going to use for user creation
            logger.info(f"Attempting to create/update user with telegram_id: {telegram_id}")

            try:
                # First try to get the existing user
                existing_user = TelegramUser.objects.filter(telegram_id=telegram_id).first()
                logger.info(f"Existing user found: {existing_user is not None}")

                if existing_user:
                    # Update existing user
                    existing_user.first_name = first_name
                    existing_user.last_name = last_name
                    existing_user.photo_url = photo_url
                    existing_user.save()
                    logger.info(f"Updated existing user: {existing_user.telegram_id}")
                    user = existing_user
                else:
                    # Create new user
                    user = TelegramUser.objects.create(
                        telegram_id=telegram_id,
                        first_name=first_name,
                        last_name=last_name,
                        photo_url=photo_url
                    )
                    logger.info(f"Created new user: {user.telegram_id}")

                # Verify the user was saved
                verification_user = TelegramUser.objects.get(telegram_id=telegram_id)
                logger.info(f"Verification successful: User exists with ID {verification_user.telegram_id}")

                return Response({
                    'message': 'Data stored successfully',
                    'user_id': user.id,
                    'telegram_id': user.telegram_id
                }, status=status.HTTP_200_OK)

            except TelegramUser.DoesNotExist:
                logger.error(f"Failed to verify user creation for telegram_id: {telegram_id}")
                return Response({
                    'message': 'User creation failed verification',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Error while saving data: {str(e)}")
            logger.exception("Full traceback:")
            return Response({
                'message': 'Internal server error',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)