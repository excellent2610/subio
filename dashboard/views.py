from decimal import Decimal, ROUND_HALF_UP
from django.shortcuts import render
from subscriptions.models import Subscription
from datetime import date, datetime
import requests
import calendar
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Знаки валют
CURRENCY_SIGNS = {
    "UAH": "₴",
    "USD": "$",
    "EUR": "€",
}

API_KEY = "49ef0e16f185ba0f482928fe"
API_BASE = "USD"  # Базова валюта для API

def get_exchange_rates():
    """Отримати курси валют з API"""
    url = f"https://v6.exchangerate-api.com/v6/49ef0e16f185ba0f482928fe/latest/USD"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        if data['result'] == 'success':
            return {
                "USD": Decimal("1"),
                "UAH": Decimal(str(data['conversion_rates']['UAH'])),
                "EUR": Decimal(str(data['conversion_rates']['EUR'])),
            }
    except Exception as e:
        print("Помилка при отриманні курсів:", e)
    # fallback
    return {"USD": Decimal("1"), "UAH": Decimal("40"), "EUR": Decimal("0.93")}

def convert(amount: Decimal, from_currency: str, to_currency: str, rates: dict) -> Decimal:
    """Конвертація валюти Decimal → Decimal"""
    if from_currency == to_currency:
        return amount
    amount_in_usd = amount / rates[from_currency.upper()]
    return (amount_in_usd * rates[to_currency.upper()]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

@login_required(login_url='/users/login/')
def dashboard_view(request):
    # Беремо тільки підписки поточного користувача
    subscriptions = Subscription.objects.filter(user=request.user)

    # Вибір валюти
    page_currency = request.GET.get("currency", "UAH")
    if page_currency not in CURRENCY_SIGNS:
        page_currency = "UAH"

    # Фільтр за датою
    filter_date_str = request.GET.get("filter_date")
    if filter_date_str:
        try:
            filter_date = datetime.strptime(filter_date_str, "%Y-%m-%d").date()
            subscriptions = subscriptions.filter(next_payment_date=filter_date)
        except ValueError:
            pass

    today = date.today()
    total_monthly = Decimal("0.00")
    rates = get_exchange_rates()
    months = [calendar.month_name[i] for i in range(1, 13)]
    monthly_totals = [Decimal("0.00") for _ in range(12)]

    for sub in subscriptions:
        # Статус днів до наступного платежу
        if sub.next_payment_date:
            sub.days_left = (sub.next_payment_date - today).days
            if sub.days_left > 7:
                sub.status_class = "status-ok"
            elif 3 <= sub.days_left <= 7:
                sub.status_class = "status-warning"
            else:
                sub.status_class = "status-danger"
        else:
            sub.days_left = None
            sub.status_class = "status-ok"

        # Місячний платіж
        if sub.billing_cycle == "yearly":
            monthly_price = (sub.price / Decimal("12")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            monthly_price = sub.price

        monthly_converted = convert(sub.price, sub.currency.upper(), page_currency, rates)
        total_monthly += monthly_converted

        # Графік по місяцях
        if sub.next_payment_date:
            month_index = sub.next_payment_date.month - 1
            monthly_totals[month_index] += monthly_converted

    context = {
        "subscriptions": subscriptions,
        "total_monthly": f"{total_monthly:.2f}",
        "page_currency": page_currency,
        "currency_sign": CURRENCY_SIGNS.get(page_currency, "₴"),
        "months": months,
        "monthly_totals": [float(x) for x in monthly_totals],
        "request": request,
    }

    return render(request, "dashboard/dashboard.html", context)

# --- AJAX для оновлення графіку ---
def dashboard_ajax(request):
    subscriptions = Subscription.objects.all()
    page_currency = request.GET.get("currency", "UAH")
    if page_currency not in CURRENCY_SIGNS:
        page_currency = "UAH"

    rates = get_exchange_rates()
    monthly_totals = [Decimal("0.00") for _ in range(12)]
    today = date.today()

    for sub in subscriptions:
        if sub.billing_cycle == "yearly":
            monthly_price = (sub.price / Decimal("12")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            monthly_price = sub.price

        monthly_converted = convert(monthly_price, sub.currency.upper(), page_currency, rates)
        if sub.next_payment_date:
            month_index = sub.next_payment_date.month - 1
            monthly_totals[month_index] += monthly_converted

    months = [calendar.month_name[i] for i in range(1, 13)]
    total_monthly = sum(monthly_totals)

    return JsonResponse({
        "months": months,
        "monthly_totals": [float(x) for x in monthly_totals],
        "currency_sign": CURRENCY_SIGNS.get(page_currency, "₴"),
        "total_monthly": f"{total_monthly:.2f}",
    })

@login_required
def delete_account_view(request):
    if request.method == "POST":
        request.user.delete()
        return redirect("login")
