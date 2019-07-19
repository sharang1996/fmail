#!/usr/bin/env python3
"""Celery Task Queue for FMail."""

from os.path import basename
from smtplib import SMTP
from email.message import EmailMessage
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery import Celery

ME = basename(__file__)
if ME.endswith('.py'):
    ME = ME.split('.')[:-1]

APP = Celery(ME, broker='amqp://localhost')

MAILER = SMTP('localhost')
SENDER = 'celery@localhost'


@APP.task
def sendmail(receiver_email, subject, text, sender_email, password):

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    msg = MIMEText(text, "html")

    message.attach(msg)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')
