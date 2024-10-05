from django.contrib.auth.models import AbstractUser
from django.db import models

class Player(models.Model):
    score = models.IntegerField(default=0)
    last_shot_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Player: {self.custom_user.username} - Score: {self.score}"

class CustomUser(AbstractUser):
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    telegram_username = models.CharField(max_length=255, null=True, blank=True)
    player = models.OneToOneField(Player, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} - Telegram Username: {self.telegram_username} - Telegram ID: {self.telegram_id}"