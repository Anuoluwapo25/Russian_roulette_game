from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager


class TelegramUserManager(BaseUserManager):
    def create_user(self, telegram_id, first_name, password=None, **extra_fields):
        if not telegram_id:
            raise ValueError("The Telegram ID must be set")
        user = self.model(telegram_id=telegram_id, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, first_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(telegram_id, first_name, password, **extra_fields)
    
    

class Player(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.telegram_id 


class Game(models.Model):
    current_game = models.BooleanField(default=False)
    selected_number = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def select_number(self, player, number):
        if not self.current_game:
            raise ValueError("No active game")

        player_ranges = {
            1: range(1, 6), 
            2: range(6, 11),  
            3: range(11, 16)  
        }

        if player not in player_ranges:
            raise ValueError("Invalid player number")

        if number not in player_ranges[player]:
            raise ValueError(f"Number must be in range {player_ranges[player].start}-{player_ranges[player].stop - 1}")

        self.selected_number = number
        self.save()

        return f"Player {player} selected {number}"

    def get_selected_number(self):
        return self.selected_number

    def clear_game_data(self):
        self.selected_number = None
        self.current_game = False
        self.save()

    def __str__(self):
        return f"Game by {self.user} - Selected number: {self.selected_number if self.selected_number else 'None'}"

    




