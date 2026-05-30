# accounts/utils.py

import random
from django.core.mail import send_mail
from django.conf import settings
from .models import OTP


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(user):
    # Invalidate all previous OTPs for this user
    OTP.objects.filter(user=user, is_used=False).update(is_used=True)

    # Generate new OTP
    code = generate_otp()

    # Save to database
    otp = OTP.objects.create(user=user, code=code)

    # Send email
    subject = 'HostelHub - Email Verification Code'
    message = f'''
Hi {user.username},

Your verification code for HostelHub is:

{code}

This code will expire in 10 minutes.

If you did not register on HostelHub, please ignore this email.

regards,
HostelHub Team
'''
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    return otp
