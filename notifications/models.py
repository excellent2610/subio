# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TelegramProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="telegram")
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} — {self.telegram_id}"
