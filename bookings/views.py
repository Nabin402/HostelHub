# bookings/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from hostels.models import Hostel
from .models import Booking


@login_required
def book_hostel(request, hostel_id):
    if request.user.role != 'student':
        messages.error(request, 'Only students can book hostels.')
        return redirect('hostel_detail', hostel_id=hostel_id)

    hostel = get_object_or_404(Hostel, id=hostel_id, status='approved')

    # already booked check
    if Booking.objects.filter(student=request.user, hostel=hostel).exists():
        messages.warning(request, 'You have already requested this hostel.')
        return redirect('hostel_detail', hostel_id=hostel_id)

    if request.method == 'POST':
        move_in_date = request.POST.get('move_in_date')
        message = request.POST.get('message', '')

        if not move_in_date:
            messages.error(request, 'Please select a move-in date.')
            return redirect('hostel_detail', hostel_id=hostel_id)

        Booking.objects.create(
            student=request.user,
            hostel=hostel,
            move_in_date=move_in_date,
            message=message,
            status='pending'
        )

        messages.success(
            request, f'Booking request sent to {hostel.name}! Wait for owner approval.')
        return redirect('hostel_detail', hostel_id=hostel_id)

    return redirect('hostel_detail', hostel_id=hostel_id)


@login_required
def my_bookings(request):
    if request.user.role != 'student':
        return redirect('home')

    bookings = Booking.objects.filter(
        student=request.user
    ).select_related('hostel').order_by('-created_at')

    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, student=request.user)

    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
    else:
        messages.error(request, 'Only pending bookings can be cancelled.')

    return redirect('my_bookings')
