# hostels/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.HomeView.as_view(), name='home'),
    path('hostel/<int:hostel_id>/',
         views.HostelDetailView.as_view(), name='hostel_detail'),

    # Owner
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/hostels/add/', views.add_hostel, name='add_hostel'),
    path('owner/hostels/<int:hostel_id>/edit/',
         views.edit_hostel, name='edit_hostel'),
    path('owner/hostels/<int:hostel_id>/delete/',
         views.delete_hostel, name='delete_hostel'),
    path('owner/hostels/submitted/',
         views.hostel_submitted, name='hostel_submitted'),
    path('owner/hostels/<int:hostel_id>/toggle-availability/',
         views.toggle_availability, name='toggle_availability'),
    path('owner/images/<int:image_id>/delete/',
         views.delete_hostel_image, name='delete_hostel_image'),

    # Booking actions
    path('owner/bookings/<int:booking_id>/approve/',
         views.approve_booking, name='approve_booking'),
    path('owner/bookings/<int:booking_id>/reject/',
         views.reject_booking, name='reject_booking'),

    # Admin
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/hostels/<int:hostel_id>/approve/',
         views.approve_hostel, name='approve_hostel'),
    path('admin-panel/hostels/<int:hostel_id>/reject/',
         views.reject_hostel, name='reject_hostel'),
    path('admin/delete-user/<int:user_id>/',
         views.admin_delete_user, name='admin_delete_user'),
    path('admin/delete-hostel/<int:hostel_id>/',
         views.admin_delete_hostel, name='admin_delete_hostel'),
]
