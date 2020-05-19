from threading import Thread

from flask import current_app
from flask_mail import Message, Mail

from api.config import BaseConfig


def send_async_email(application, message):
    with application.app_context():
        mail = Mail(current_app)
        mail.send(message)


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=BaseConfig.ADMINS
    )
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
