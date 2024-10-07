from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    telegram_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.username

class Player(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    wallet_connected = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class GameSession(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    result = models.IntegerField()  # Stores the outcome of the game or random number

    def __str__(self):
        return f"Game for {self.player.user.username} at {self.timestamp}"
