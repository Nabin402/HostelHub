# hostels/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/hostels/add/', views.add_hostel, name='add_hostel'),
    path('owner/hostels/<int:hostel_id>/edit/', views.edit_hostel, name='edit_hostel'),
    path('owner/hostels/<int:hostel_id>/delete/', views.delete_hostel, name='delete_hostel'),
    path('owner/bookings/<int:booking_id>/approve/', views.approve_booking, name='approve_booking'),
    path('owner/bookings/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
]
