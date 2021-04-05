import os
from flask import Flask, render_template
from flask_mail import Message
from ..app import mail


app = Flask(__name__)

class Mailing():
    """
    Mail Class
    """
    @staticmethod
    def send_mail(recipients, subject, body, html):
        try:
            msg = Message(subject,
            sender="tat_bot@sirim.my",
            recipients=recipients)
            msg.body = body
            msg.html = html
            mail.send(msg)
        except Exception as e:
            app.logger.error(e)
            raise Exception(e)