# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegisterForm, OwnerRegisterForm, LoginForm
from .models import CustomUser, OTP
from .utils import send_otp_email


def register_student(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # inactive until email verified
            user.save()
            send_otp_email(user)
            request.session['verification_user_id'] = user.id
            messages.success(
                request, 'Account created! Please check your email for the verification code.')
            return redirect('verify_email')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegisterForm()

    return render(request, 'users/register_student.html', {'form': form})


def register_owner(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = OwnerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # inactive until email verified
            user.save()
            send_otp_email(user)
            request.session['verification_user_id'] = user.id
            messages.success(
                request, 'Account created! Please check your email for the verification code.')
            return redirect('verify_email')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OwnerRegisterForm()

    return render(request, 'users/register_owner.html', {'form': form})


def verify_email(request):
    user_id = request.session.get('verification_user_id')

    if not user_id:
        messages.error(request, 'Session expired. Please register again.')
        return redirect('register_student')

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('register_student')

    if request.method == 'POST':
        code = request.POST.get('code')

        otp = OTP.objects.filter(user=user, code=code, is_used=False).last()

        if otp and otp.is_valid():
            otp.is_used = True
            otp.save()
            user.is_active = True
            user.is_email_verified = True
            user.save()
            login(request, user)
            del request.session['verification_user_id']
            messages.success(
                request, f'Email verified! Welcome to HostelHub, {user.username}!')
            return redirect_by_role(user)
        else:
            messages.error(
                request, 'Invalid or expired OTP. Please try again.')

    return render(request, 'users/verifiy_email.html', {'email': user.email})


def resend_otp(request):
    user_id = request.session.get('verification_user_id')

    if not user_id:
        messages.error(request, 'Session expired. Please register again.')
        return redirect('register_student')

    try:
        user = CustomUser.objects.get(id=user_id)
        send_otp_email(user)
        messages.success(
            request, 'A new verification code has been sent to your email.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')

    return redirect('verify_email')


def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not user.is_email_verified:
                    request.session['verification_user_id'] = user.id
                    send_otp_email(user)
                    messages.warning(
                        request, 'Please verify your email first.')
                    return redirect('verify_email')
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect_by_role(user)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def redirect_by_role(user):
    if user.role == 'owner':
        return redirect('owner_dashboard')
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.address = request.POST.get('address', user.address)

        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'accounts/profile.html', {'user': user})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
        elif new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            messages.success(
                request, 'Password changed successfully. Please log in again.')
            return redirect('login')

    return render(request, 'users/change_password.html')
