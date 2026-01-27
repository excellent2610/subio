from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(blank=True, null=True)

    # Додаємо related_name до полів, щоб уникнути конфлікту
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # <-- змінено
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # <-- змінено
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    telegram_id = models.BigIntegerField(null=True, blank=True)

    
    def __str__(self):
        return self.username
