from celery import shared_task
import asyncio

@shared_task
def send_telegram_message(chat_id: int, text: str):
    """
    Відправка одноразового повідомлення через Celery.
    """
    asyncio.run(send_message_async(chat_id, text))

@shared_task
def send_automatic_notification(chat_id: int):
    """
    Автоматичне повідомлення (можна викликати раз на день/годину)
    """
    message = "Це автоматичне повідомлення від Subio Bot!"
    asyncio.run(send_message_async(chat_id, message))
