from django.conf import settings
from django.core.mail import send_mail

from project.celery import app


@app.task
def send_notification_mail(user_mail, user_comment_text, user_comment_date, sender_username,  product_title, url):
    send_mail(
        'Кто-то ответил на ваш комментарий',
        f'Пользователь под ником {sender_username} оставил ответ на ваш комментарий под товаром {product_title}: '
        f'"{user_comment_text}" {user_comment_date}. Перейдите по ссылке, чтобы увидеть ответ {url}',
        settings.EMAIL_HOST_USER,
        [user_mail],
        fail_silently=False,
    )
