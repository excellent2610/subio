from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Subscription
from .forms import SubscriptionForm
from datetime import date
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse

@login_required
def add_subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            messages.success(request, "Підписка додана успішно!")
            return redirect('dashboard:dashboard')
    else:
        form = SubscriptionForm()
    return render(request, 'subscriptions/add_subscription.html', {'form': form})


@login_required
def subscription_edit(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == "POST":
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard')
    else:
        form = SubscriptionForm(instance=subscription)
    return render(request, "subscriptions/add_subscription.html", {"form": form})


@login_required
def subscription_delete(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == "POST":
        subscription.delete()
        return redirect('dashboard:dashboard')
    return render(request, "subscriptions/subscription_confirm_delete.html", {"subscription": subscription})

def mark_paid(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)
    if request.method == "POST":
        # Переносимо next_payment_date на 1 місяць вперед
        if subscription.next_payment_date:
            from dateutil.relativedelta import relativedelta
            subscription.next_payment_date += relativedelta(months=+1)
        else:
            # Якщо дати не було, ставимо сьогодні + 1 місяць
            subscription.next_payment_date = timezone.now().date() + relativedelta(months=+1)
        subscription.save()
    return redirect('dashboard:dashboard')  # або твій url для дашборду

@login_required
def cancel_subscription(request):
    if request.method != 'POST':
        return JsonResponse({'success': False})

    subscription = getattr(request.user, 'subscription', None)

    if not subscription:
        return JsonResponse({
            'success': False,
            'error': 'Підписку не знайдено'
        })

    subscription.is_active = False
    subscription.save()

    return JsonResponse({'success': True})

@login_required
def plans(request):
    return render(request, 'subscriptions/plans.html')