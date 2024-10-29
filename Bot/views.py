from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from telegram import Update
from rest_framework import generics
from django.db import transaction
from telegram.ext import Application
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import os
import os.path
import json
import logging
from asgiref.sync import async_to_sync
from .models import Player, Game, TelegramUser




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
            with transaction.atomic():  # Start atomic transaction
                logger.info("Transaction started")
                data = request.data

                telegram_id = str(data.get('id'))
                first_name = data.get('first_name')
                last_name = data.get('last_name', '')
                photo_url = data.get('photo_url', None)
                auth_date = data.get('auth_date')

                if not telegram_id:
                    logger.error("Missing telegram_id in request")
                    return Response({
                        'message': 'telegram_id (id) is required'
                    }, status=status.HTTP_400_BAD_REQUEST)

                logger.info(f"Attempting to create/update user with telegram_id: {telegram_id}")

                # Use update_or_create to either update an existing user or create a new one
                user, created = TelegramUser.objects.update_or_create(
                    telegram_id=telegram_id,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'photo_url': photo_url
                    }
                )

                if created:
                    logger.info(f"Created new user: {user.telegram_id}")
                else:
                    logger.info(f"Updated existing user: {user.telegram_id}")

                # Log user ID for verification
                logger.info(f"User with telegram_id {telegram_id} has ID {user.id}")

                # Verify the user was saved
                verification_user = TelegramUser.objects.get(telegram_id=telegram_id)
                logger.info(f"Verification successful: User exists with ID {verification_user.telegram_id}")

                logger.info("Preparing to return successful response")
                
                # Log success in the response
                logger.info("Data stored successfully")

                return Response({
                    'message': 'Data stored successfully',
                    'user_id': user.id,
                    'telegram_id': user.telegram_id
                }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error while saving data: {str(e)}")
            logger.exception("Full traceback:", exc_info=True)
            return Response({
                'message': 'Internal server error',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def select_number_view(request):
    user = request.user  # The authenticated TelegramUser
    player = request.data.get('player')  # e.g., Player 1, Player 2, etc.
    number = request.data.get('number')  # The number the player is selecting

    # Ensure the player and number are provided
    if player is None or number is None:
        return Response({"error": "Player and number must be provided."}, status=400)

    # Get or create a game for the user
    game, created = Game.objects.get_or_create(user=user, current_game=True)

    try:
        # Let the user select a number
        message = game.select_number(player, number)
        return Response({"message": message}, status=200)
    except ValueError as e:
        return Response({"error": str(e)}, status=400)
    

@api_view(['POST'])
def spin_wheel(request):
    # Your logic for spinning the wheel goes here
    return Response({"message": "Wheel spun"}, status=status.HTTP_200_OK)