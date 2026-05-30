# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
# immports for otp generation
import random
import string
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('owner', 'Hostel Owner'),
        ('admin', 'Admin'),
    )
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)
    is_email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to='profiles/', blank=True, null=True)
    address = models.TextField(blank=True)

    def is_student(self):
        return self.role == 'student'

    def is_owner(self):
        return self.role == 'owner'

    def is_admin_user(self):
        return self.role == 'admin'


class OTP(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # OTP expires after 10 minutes
        expiry_time = self.created_at + timedelta(minutes=10)
        return timezone.now() < expiry_time and not self.is_used

    def __str__(self):
        return f"OTP for {self.user.username} - {self.code}"
