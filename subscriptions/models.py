from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Subscription(models.Model):
    BILLING_CHOICES = [
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("canceled", "Canceled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=5, default="USD")
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CHOICES)
    next_payment_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name

    def is_due_soon(self):
        """Повертає True, якщо залишилося <= 7 днів до наступної оплати"""
        return (self.next_payment_date - timezone.now().date()).days <= 7

    def get_status_class(self):
        """
        Метод для визначення кольору рамки підписки:
        - status-ok: активна і не скоро платіж
        - status-warning: скоро платіж
        - status-danger: скасована
        """
        if self.status == "canceled":
            return "status-danger"
        elif self.is_due_soon():
            return "status-warning"
        elif self.status == "active":
            return "status-ok"
        return ""

    def mark_paid(self):
        """
        Оновлює дату наступного платежу залежно від циклу оплати
        Викликається при натисканні кнопки "Сплачено"
        """
        if self.billing_cycle == "monthly":
            self.next_payment_date += timedelta(days=30)
        elif self.billing_cycle == "yearly":
            self.next_payment_date += timedelta(days=365)
        self.save()
