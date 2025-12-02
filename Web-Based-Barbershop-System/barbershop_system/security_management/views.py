from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):
    """User registration view"""
    if request.method == 'POST':
        # Handle registration logic here
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('security:login')

    return render(request, 'security/register.html')


@login_required
def profile(request):
    """User profile view"""
    return render(request, 'security/profile.html', {'user': request.user})
