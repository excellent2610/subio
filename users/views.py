from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from subscriptions.models import Subscription
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard:index")
    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вхід успішний!")
            return redirect("dashboard:dashboard")
        else:
            messages.error(request, "Неправильний логін або пароль.")
    else:
        form = CustomAuthenticationForm()
    return render(request, "users/login.html", {"form": form})


@login_required
def update_username(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_username = data.get("username", "").strip()
            
            if not new_username:
                return JsonResponse({"status": "error", "error": "Нік не може бути порожнім"})

            # Перевірка, чи такий нік уже існує
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
                return JsonResponse({"status": "error", "error": "Такий нік уже зайнятий"})

            # Зберігаємо нік
            request.user.username = new_username
            request.user.save()

            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "error", "error": str(e)})

    return JsonResponse({"status": "error", "error": "Невірний метод запиту"})


def logout_view(request):
    logout(request)
    messages.success(request, "Ви вийшли з акаунту.")
    return redirect("users:login")

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        # Видаляємо всі підписки користувача
        Subscription.objects.filter(user=user).delete()
        # Видаляємо акаунт
        user.delete()
        # Виходимо з сесії
        logout(request)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Невірний метод"})


@csrf_protect
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Акаунт створено")
            return redirect("users:login")
    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {
        "form": form
    })

@ensure_csrf_cookie
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Метод не дозволений'}, status=405)

@login_required
def logout_confirm_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("users:login")
    return render(request, "users/logout_confirm.html")

@login_required
def delete_account_confirm_view(request):
    if request.method == "POST":
        user = request.user
        user.delete()  # видаляємо акаунт
        messages.success(request, "Акаунт успішно видалено")
        logout(request)
        return redirect("users:login")
    return render(request, "users/delete_account_confirm.html")

@login_required
def delete_account_view(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect("login")  # після видалення повертаємо на логін
    return redirect("dashboard")  # якщо хтось зайшов GET