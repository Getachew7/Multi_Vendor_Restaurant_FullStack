from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings

def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl

def activateEmail(request, user):
    from_email = settings.DEFULT_FROM_EMAIL
    mail_subject = 'Please activate your account'
    context = {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    }
    message = render_to_string('account/emails/account_verification_email.html', context=context)
    email = EmailMessage(mail_subject, message, from_email, to=[user.email])
    if email.send():
        messages.success(request, f"Please go to your email {user.email} inbox and click on recived activation link to confirm and compelet the registration. Note: Check your spam folder.")
    else:
        messages.error(request, f'Problem sending email to {user.email}, Check if you typed it correctly')

def send_password_reset_email(request, user):
    from_email = settings.DEFULT_FROM_EMAIL
    mail_subject = 'Reset your password'
    context = {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    }
    message = render_to_string('account/emails/reset_password_email.html', context=context)
    email = EmailMessage(mail_subject, message, from_email, to=[user.email])
    email.send()
  