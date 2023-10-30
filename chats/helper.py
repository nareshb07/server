from django.core.mail import send_mail
from django.conf import settings 
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_forget_password_mail(email , token ):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/chats/change-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True



def send_PaymentSuccess_mail_to_Follower(email, order):
    subject = 'Payment Successful'
    message = render_to_string('follower_payment_success.html',{"Order_obj":order})
    plain_message = strip_tags(message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def send_PaymentSuccess_mail_to_Creator(email, order):
    subject = 'Payment Successful'
    message = render_to_string('creator_payment_success.html',{"Order_obj":order})
    plain_message = strip_tags(message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

    