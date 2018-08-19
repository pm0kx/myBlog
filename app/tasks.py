#encoding: utf-8
import smtplib
import datetime
from email.mime.text import MIMEText
from flask_mail import Message
from flask import render_template
from app.models import Mail
#from app.common.extensions import flask_celery
from app.common.extensions import mail
from threading import Thread

# from app import create_app
# app = create_app('development' or 'default')
#
# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)
#
#
# def send_email(to, subject, template, **kwargs):
#     msg = Message(subject=subject,
#                            sender=app.config['MAIL_SENDER'],
#                            recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr
#
#
# def send_email_demo(to, subject,app):
#     msg = Message(subject=subject,
#                            sender=app.config['MAIL_SENDER'],
#                            recipients=[to])
#     msg.body = "testing"
#     msg.html = "<b>testing</b>"
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr


# @flask_celery.task(bind=True,igonre_result=True,default_retry_delay=300,max_retries=5)
# def mail_remind(self, primary_key):
#     """Send the remind email to user when registered.
#        Using Flask-Mail.
#     """
#
#     reminder = Mail.query.get(primary_key)
#     msg = MIMEText(reminder.text)
#
#     msg = Message(subject='flask mail test',
#                       sender="zhu14623@163.com",
#                       recipients=[reminder.email])
#     msg.body = reminder.text
#
#     mail.send(msg)
#
#
# def on_reminder_save(mapper, connect, self):
#     """Callbask for task remind."""
#     mail_remind.apply_async(args=(self.id), eta=self.date)