from flask import current_app
from flask_mail import Message, Mail

from api.config import BaseConfig


def send_email(to, subject, template):
    mail = Mail(current_app)
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=BaseConfig.ADMINS
    )
    mail.send(msg)
