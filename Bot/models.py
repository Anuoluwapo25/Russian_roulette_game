from django.db import models
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
    

class TelegramUser(AbstractUser):
    telegram_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)
    auth_date = models.DateTimeField(auto_now_add=True)

    username = None 
    USERNAME_FIELD = 'telegram_id' 
    REQUIRED_FIELDS = ['first_name'] 

    objects = TelegramUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.telegram_id})"
    


class Player(models.Model):
    user = models.OneToOneField(TelegramUser, on_delete=models.CASCADE, null=True) 
    wallet_connected = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.telegram_id 


class GameSession(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    result = models.IntegerField() 

    def __str__(self):
        return f"Game for {self.player.user.telegram_id} at {self.timestamp}"

