from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User


def register(request):
    """User registration view"""
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone_number = request.POST.get('phone_number', '')

        # Validate passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'security/register.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'security/register.html')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'security/register.html')

        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                role='customer'  # Default role
            )

            messages.success(request, 'Registration successful! Please log in.')
            return redirect('security:login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'security/register.html')

    return render(request, 'security/register.html')


@login_required
def profile(request):
    """User profile view"""
    if request.method == 'POST':
        # Update profile
        try:
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.phone_number = request.POST.get('phone_number', '')

            # Handle date of birth
            date_of_birth = request.POST.get('date_of_birth', '')
            if date_of_birth:
                user.date_of_birth = date_of_birth

            # Handle profile picture
            if 'profile_picture' in request.FILES:
                user.profile_picture = request.FILES['profile_picture']

            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('security:profile')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')

    return render(request, 'security/profile.html', {'user': request.user})
