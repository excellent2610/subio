from django import forms
from .models import Subscription

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['service_name', 'price', 'currency', 'billing_cycle', 'next_payment_date']
        widgets = {
            'service_name': forms.TextInput(attrs={
                'class': 'input-field example', 'placeholder': 'Наприклад: Netflix'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'input-field example', 'placeholder': 'Наприклад: 10.99'
            }),
            'currency': forms.TextInput(attrs={
                'class': 'input-field currency-select', 'placeholder': 'USD'
            }),
            'billing_cycle': forms.Select(attrs={
                'class': 'input-field cycle-payment'
            }),
            'next_payment_date': forms.DateInput(attrs={
                'class': 'input-field', 'type': 'date'
            }),
        }
