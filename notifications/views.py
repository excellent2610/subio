from django.http import JsonResponse
from .tasks import send_telegram_message
from django.contrib.auth.decorators import login_required

def get_my_chat_id(request):
    """
    Повертає chat_id користувача після натискання кнопки в Telegram (через webhook або ручний виклик).
    """
    # Для простоти: передаємо chat_id як параметр GET
    chat_id = request.GET.get("chat_id")
    if not chat_id:
        return JsonResponse({"status": "error", "message": "Chat ID не передано"}, status=400)
    return JsonResponse({"status": "ok", "chat_id": int(chat_id)})

def send_test_message(request):
    """
    Відправка тестового одноразового повідомлення.
    Передає chat_id через GET-параметр.
    """
    chat_id = request.GET.get("chat_id")
    if not chat_id:
        return JsonResponse({"status": "error", "message": "Chat ID не передано"}, status=400)

    send_telegram_message.delay(int(chat_id), "Привіт! Це тестове повідомлення через Celery.")
    return JsonResponse({"status": "ok", "message": "Повідомлення відправлено!"})

def send_test_message(request):
    """
    Відправка тестового одноразового повідомлення.
    Передає chat_id через GET-параметр.
    """
    chat_id = request.GET.get("chat_id")
    if not chat_id:
        return JsonResponse({"status": "error", "message": "Chat ID не передано"}, status=400)

    send_telegram_message.delay(int(chat_id), "Привіт! Це тестове повідомлення через Celery.")
    return JsonResponse({"status": "ok", "message": "Повідомлення відправлено!"})

@login_required
def test_notification(request):
    return JsonResponse({'success': True})
