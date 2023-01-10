from conf.celery import app
from .service import send


@app.task
def silent_send(user_email):
    send(user_email)
