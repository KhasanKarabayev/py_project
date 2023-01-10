from conf.celery import app
from .service import send
from .models import Mail  # Для Запуска задач по расписанию


@app.task
def silent_send(user_email):
    """Выполнение CPU-bound задач в фоне в Django"""
    send(user_email)


@app.task
def send_spam():
    """Запуск задач по расписанию"""
    for user_email in Mail.objects.all():
        send(user_email)

