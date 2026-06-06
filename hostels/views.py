# hostels/views.py

from datetime import date
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from bookings.models import Booking
from .forms import HostelForm, ReviewForm
from .models import Hostel, HostelImage, Review


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        hostels = Hostel.objects.filter(status='approved')

        location = request.GET.get('location', '').strip()
        hostel_type = request.GET.get('hostel_type', '').strip()
        room_type = request.GET.get('room_type', '').strip()
        max_price = request.GET.get('max_price', '').strip()

        if location:
            hostels = hostels.filter(
                Q(city__icontains=location) |
                Q(address__icontains=location)
            )
        if hostel_type:
            hostels = hostels.filter(hostel_type=hostel_type)
        if room_type:
            hostels = hostels.filter(room_type=room_type)
        if max_price:
            try:
                hostels = hostels.filter(price_per_month__lte=float(max_price))
            except ValueError:
                pass

        is_filtered = any([location, hostel_type, room_type, max_price])
        featured_hostels = hostels.order_by('-created_at')
        if not is_filtered:
            featured_hostels = featured_hostels[:6]

        return render(request, self.template_name, {
            'featured_hostels': featured_hostels,
            'is_filtered': is_filtered,
            'result_count': hostels.count() if is_filtered else None,
        })

class HostelDetailView(View):
    template_name = 'hostels/hostel_detail.html'

    def get(self, request, hostel_id):
        hostel = get_object_or_404(Hostel, id=hostel_id, status='approved')
        images = hostel.images.all()
        primary_image = images.filter(
            is_primary=True).first() or images.first()

        has_booked = False
        has_reviewed = False
        review_form = None

        if request.user.is_authenticated:
            has_booked = Booking.objects.filter(
                student=request.user, hostel=hostel
            ).exists()
            has_reviewed = Review.objects.filter(
                student=request.user, hostel=hostel
            ).exists()
            if request.user.role == 'student' and not has_reviewed:
                review_form = ReviewForm()

        reviews = hostel.reviews.select_related('student').all()

        return render(request, self.template_name, {
            'hostel': hostel,
            'images': images,
            'primary_image': primary_image,
            'has_booked': has_booked,
            'has_reviewed': has_reviewed,
            'review_form': review_form,
            'reviews': reviews,
            'today': date.today(),
        })

    def post(self, request, hostel_id):
        hostel = get_object_or_404(Hostel, id=hostel_id, status='approved')

        if not request.user.is_authenticated or request.user.role != 'student':
            messages.error(request, 'Only students can leave reviews.')
            return redirect('hostel_detail', hostel_id=hostel_id)

        already_reviewed = Review.objects.filter(
            student=request.user, hostel=hostel).exists()
        if already_reviewed:
            messages.warning(request, 'You have already reviewed this hostel.')
            return redirect('hostel_detail', hostel_id=hostel_id)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.hostel = hostel
            review.student = request.user
            review.save()
            messages.success(request, 'Review submitted successfully!')
        else:
            messages.error(request, 'Please fix the errors in your review.')

        return redirect('hostel_detail', hostel_id=hostel_id)


@login_required
def toggle_availability(request, hostel_id):
    """Owner can toggle hostel availability on/off."""
    if request.user.role != 'owner':
        return redirect('home')

    hostel = get_object_or_404(Hostel, id=hostel_id, owner=request.user)
    hostel.is_available = not hostel.is_available
    hostel.save()

    status = 'available' if hostel.is_available else 'marked as fully booked'
    messages.success(request, f'"{hostel.name}" is now {status}.')
    return redirect('hostel_detail', hostel_id=hostel_id)


@login_required
def delete_hostel_image(request, image_id):
    """Owner can delete individual hostel images."""
    image = get_object_or_404(HostelImage, id=image_id)
    hostel = image.hostel

    if request.user != hostel.owner:
        messages.error(request, 'Permission denied.')
        return redirect('home')

    image.delete()
    messages.success(request, 'Image deleted.')
    return redirect('edit_hostel', hostel_id=hostel.id)


@login_required
def owner_dashboard(request):
    if request.user.role != 'owner':
        messages.error(request, 'Access denied.')
        return redirect('home')

    hostels = Hostel.objects.filter(owner=request.user).order_by('-created_at')
    bookings = Booking.objects.filter(
        hostel__owner=request.user
    ).select_related('student', 'hostel').order_by('-created_at')[:6]

    context = {
        'hostels': hostels,
        'bookings': bookings,
        'total_hostels': hostels.count(),
        'pending_approval_count': hostels.filter(status='pending').count(),
        'active_bookings_count': Booking.objects.filter(
            hostel__owner=request.user, status='approved').count(),
        'total_requests_count': Booking.objects.filter(
            hostel__owner=request.user).count(),
        'pending_booking_count': Booking.objects.filter(
            hostel__owner=request.user, status='pending').count(),
    }
    return render(request, 'hostels/owner_dashboard.html', context)


AMENITIES = [
    ('has_wifi',        'bi-wifi',          'WiFi'),
    ('has_parking',     'bi-p-circle',      'Parking'),
    ('has_laundry',     'bi-water',         'Laundry'),
    ('has_hot_water',   'bi-droplet',       'Hot Water'),
    ('has_cctv',        'bi-camera-video',  'CCTV'),
    ('has_kitchen',     'bi-cup-hot',       'Kitchen'),
    ('has_meals',       'bi-egg-fried',     'Meals Included'),
    ('has_study_room',  'bi-book',          'Study Room'),
    ('has_power_backup', 'bi-lightning',     'Power Backup'),
]


@login_required
def add_hostel(request):
    if request.user.role != 'owner':
        messages.error(request, 'Only hostel owners can add hostels.')
        return redirect('home')

    if request.method == 'POST':
        form = HostelForm(request.POST)
        images = request.FILES.getlist('images')

        if form.is_valid():
            hostel = form.save(commit=False)
            hostel.owner = request.user
            hostel.status = 'pending'
            hostel.save()

            for index, image in enumerate(images):
                HostelImage.objects.create(
                    hostel=hostel,
                    image=image,
                    is_primary=(index == 0)
                )

            messages.success(
                request,
                f'Hostel "{hostel.name}" submitted! It will go live after admin approval.'
            )
            return redirect('hostel_submitted')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = HostelForm()

    return render(request, 'hostels/add_hostel.html', {
        'form': form,
        'amenities': AMENITIES,
    })


@login_required
def edit_hostel(request, hostel_id):
    if request.user.role != 'owner':
        return redirect('home')

    hostel = get_object_or_404(Hostel, id=hostel_id, owner=request.user)

    if request.method == 'POST':
        form = HostelForm(request.POST, instance=hostel)
        images = request.FILES.getlist('images')

        if form.is_valid():
            form.save()

            for image in images:
                HostelImage.objects.create(
                    hostel=hostel,
                    image=image,
                    is_primary=False
                )

            messages.success(request, f'Hostel "{hostel.name}" updated.')
            return redirect('owner_dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = HostelForm(instance=hostel)

    return render(request, 'hostels/edit_hostel.html', {
        'form': form,
        'hostel': hostel,
        'images': hostel.images.all(),
        'amenities': AMENITIES,
    })


@login_required
def delete_hostel(request, hostel_id):
    if request.user.role != 'owner':
        return redirect('home')

    hostel = get_object_or_404(Hostel, id=hostel_id, owner=request.user)

    if request.method == 'POST':
        hostel_name = hostel.name
        hostel.delete()
        messages.success(request, f'Hostel "{hostel_name}" deleted.')
        return redirect('owner_dashboard')

    return render(request, 'hostels/delete_hostel.html', {'hostel': hostel})


@login_required
def hostel_submitted(request):
    return render(request, 'hostels/hostel_submitted.html')


@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(
        Booking, id=booking_id, hostel__owner=request.user)
    booking.status = 'approved'
    booking.save()
    messages.success(request, 'Booking approved.')
    return redirect('owner_dashboard')


@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(
        Booking, id=booking_id, hostel__owner=request.user)
    booking.status = 'rejected'
    booking.save()
    messages.success(request, 'Booking rejected.')
    return redirect('owner_dashboard')


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('home')

    from users.models import CustomUser

    context = {
        'total_hostels': Hostel.objects.count(),
        'pending_hostels': Hostel.objects.filter(status='pending'),
        'approved_count': Hostel.objects.filter(status='approved').count(),
        'rejected_count': Hostel.objects.filter(status='rejected').count(),
        'total_students': CustomUser.objects.filter(role='student').count(),
        'total_owners': CustomUser.objects.filter(role='owner').count(),
        'all_users': CustomUser.objects.exclude(role='admin').order_by('-date_joined'),
        'recent_hostels': Hostel.objects.all().order_by('-created_at')[:5],
    }
    return render(request, 'hostels/admin_dashboard.html', context)


@login_required
def approve_hostel(request, hostel_id):
    if request.user.role != 'admin':
        return redirect('home')
    hostel = get_object_or_404(Hostel, id=hostel_id)
    hostel.status = 'approved'
    hostel.save()
    messages.success(request, f'"{hostel.name}" approved.')
    return redirect('admin_dashboard')


@login_required
def reject_hostel(request, hostel_id):
    if request.user.role != 'admin':
        return redirect('home')
    hostel = get_object_or_404(Hostel, id=hostel_id)
    hostel.status = 'rejected'
    hostel.save()
    messages.warning(request, f'"{hostel.name}" rejected.')
    return redirect('admin_dashboard')
