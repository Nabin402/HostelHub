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
    ROOM_TYPE_CHOICES = (
        ('1_seater', '1 Seater (Single Room)'),
        ('2_seater', '2 Seater (Shared - 2 Beds)'),
        ('3_seater', '3 Seater (Shared - 3 Beds)'),
        ('4_seater', '4 Seater (Shared - 4 Beds)'),
    )
    MINIMUM_STAY_CHOICES = (
        (1, '1 Month'),
        (3, '3 Months'),
        (6, '6 Months'),
        (12, '1 Year'),
    )

    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='hostels')
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    description = models.TextField()
    hostel_type = models.CharField(max_length=10, choices=HOSTEL_TYPE_CHOICES)
    room_type = models.CharField(
        max_length=20, choices=ROOM_TYPE_CHOICES, default='1_seater')
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    total_rooms = models.PositiveIntegerField()
    available_rooms = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    admission_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    # Contact
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    # Amenities — existing
    has_wifi = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    has_laundry = models.BooleanField(default=False)
    has_hot_water = models.BooleanField(default=False)
    has_cctv = models.BooleanField(default=False)
    has_kitchen = models.BooleanField(default=False)

    # Amenities — new
    has_meals = models.BooleanField(default=False)
    has_study_room = models.BooleanField(default=False)
    has_power_backup = models.BooleanField(default=False)

    # Extra info
    nearby_landmarks = models.CharField(max_length=300, blank=True, null=True)
    minimum_stay = models.PositiveIntegerField(
        choices=MINIMUM_STAY_CHOICES, default=1)
    hostel_rules = models.TextField(blank=True, null=True)

    # Location for map
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)

    # Availability toggle
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None

    def review_count(self):
        return self.reviews.count()


class HostelImage(models.Model):
    hostel = models.ForeignKey(
        Hostel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hostels/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.hostel.name}"


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    )

    hostel = models.ForeignKey(
        Hostel, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # One review per student per hostel
        unique_together = ('hostel', 'student')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.username} → {self.hostel.name} ({self.rating}★)"
