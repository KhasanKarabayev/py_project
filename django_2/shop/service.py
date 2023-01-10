from django.core.mail import send_mail
from conf import settings


def send(user_email):
    send_mail(
        subject='shop.distro.uz',
        message="Вы подписались на shop.distro.uz, мы будем отправлять вам много спама",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False
    )


