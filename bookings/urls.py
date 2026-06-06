# bookings/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:hostel_id>/', views.book_hostel, name='book_hostel'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('notifications/<int:notification_id>/read/',
         views.mark_notification_read, name='mark_notification_read'),
]
