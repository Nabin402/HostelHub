# bookings/models.py

from django.db import models
from users.models import CustomUser
from hostels.models import Hostel


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )

    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='bookings')
    hostel = models.ForeignKey(
        Hostel, on_delete=models.CASCADE, related_name='bookings')
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    move_in_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} → {self.hostel.name} ({self.status})"


class SavedHostel(models.Model):
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='saved_hostels')
    hostel = models.ForeignKey(
        Hostel, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'hostel')


class Notification(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
