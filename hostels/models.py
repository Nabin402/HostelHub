# hostels/models.py

from django.db import models
from users.models import CustomUser


class Hostel(models.Model):
    HOSTEL_TYPE_CHOICES = (
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('mixed', 'Mixed'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='hostels')
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    description = models.TextField()
    hostel_type = models.CharField(max_length=10, choices=HOSTEL_TYPE_CHOICES)
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    total_rooms = models.PositiveIntegerField()
    available_rooms = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    # Amenities
    has_wifi = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_laundry = models.BooleanField(default=False)
    has_hot_water = models.BooleanField(default=False)
    has_cctv = models.BooleanField(default=False)
    has_kitchen = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class HostelImage(models.Model):
    hostel = models.ForeignKey(
        Hostel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hostels/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.hostel.name}"
