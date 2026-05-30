# hostels/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views import View
from bookings.models import Booking
from .models import Hostel


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        featured_hostels = Hostel.objects.filter(status='approved').order_by('-created_at')[:6]
        return render(request, self.template_name, {'featured_hostels': featured_hostels})


@login_required
def owner_dashboard(request):
    hostels = Hostel.objects.filter(owner=request.user).order_by('-created_at')
    bookings = Booking.objects.filter(hostel__owner=request.user).select_related(
        'student', 'hostel'
    ).order_by('-created_at')[:6]

    context = {
        'hostels': hostels,
        'bookings': bookings,
        'total_hostels': hostels.count(),
        'pending_approval_count': hostels.filter(status='pending').count(),
        'active_bookings_count': Booking.objects.filter(
            hostel__owner=request.user,
            status='approved',
        ).count(),
        'total_requests_count': Booking.objects.filter(hostel__owner=request.user).count(),
        'pending_booking_count': Booking.objects.filter(
            hostel__owner=request.user,
            status='pending',
        ).count(),
    }
    return render(request, 'hostels/owner_dashboard.html', context)


@login_required
def add_hostel(request):
    messages.info(request, 'Add hostel form is the next feature to build.')
    return redirect('owner_dashboard')


@login_required
def edit_hostel(request, hostel_id):
    messages.info(request, 'Edit hostel form is not ready yet.')
    return redirect('owner_dashboard')


@login_required
def delete_hostel(request, hostel_id):
    messages.info(request, 'Delete hostel action is not ready yet.')
    return redirect('owner_dashboard')


@login_required
def approve_booking(request, booking_id):
    booking = Booking.objects.filter(id=booking_id, hostel__owner=request.user).first()
    if booking:
        booking.status = 'approved'
        booking.save()
        messages.success(request, 'Booking request approved.')
    return redirect('owner_dashboard')


@login_required
def reject_booking(request, booking_id):
    booking = Booking.objects.filter(id=booking_id, hostel__owner=request.user).first()
    if booking:
        booking.status = 'rejected'
        booking.save()
        messages.success(request, 'Booking request rejected.')
    return redirect('owner_dashboard')
