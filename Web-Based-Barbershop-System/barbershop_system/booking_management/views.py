from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Service, Booking, Customer


def home(request):
    """Home page view"""
    # Get popular services for display
    services = Service.objects.filter(is_active=True)[:6]

    context = {
        'services': services,
    }

    return render(request, 'booking_management/home.html', context)


def services_list(request):
    """Services listing page"""
    category = request.GET.get('category')

    if category:
        services = Service.objects.filter(is_active=True, category=category)
    else:
        services = Service.objects.filter(is_active=True)

    context = {
        'services': services,
    }

    return render(request, 'booking_management/services.html', context)


@login_required
def book_appointment(request):
    """Book appointment page"""
    if request.method == 'POST':
        # Get or create customer
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(
                user=request.user,
                first_name=request.user.first_name or request.POST.get('customer_name', '').split()[0],
                last_name=request.user.last_name or ' '.join(request.POST.get('customer_name', '').split()[1:]),
                email=request.user.email or request.POST.get('customer_email', ''),
                phone_number=request.POST.get('customer_phone', '')
            )

        # Create booking
        try:
            booking = Booking.objects.create(
                customer=customer,
                service_id=request.POST.get('service'),
                barber_id=request.POST.get('barber') if request.POST.get('barber') else None,
                booking_date=request.POST.get('booking_date'),
                booking_time=request.POST.get('booking_time'),
                notes=request.POST.get('notes', '')
            )
            messages.success(request, f'Booking created successfully! Booking ID: {booking.id}')
            return redirect('booking:my_bookings')
        except Exception as e:
            messages.error(request, f'Error creating booking: {str(e)}')

    # Get services and barbers for form
    services = Service.objects.filter(is_active=True)
    from security_management.models import User
    barbers = User.objects.filter(role='barber')

    context = {
        'services': services,
        'barbers': barbers,
    }

    return render(request, 'booking_management/book.html', context)


@login_required
def my_bookings(request):
    """Customer's bookings page"""
    try:
        customer = Customer.objects.get(user=request.user)
        bookings = Booking.objects.filter(customer=customer).order_by('-booking_date', '-booking_time')
    except Customer.DoesNotExist:
        bookings = []

    context = {
        'bookings': bookings,
    }

    return render(request, 'booking_management/my_bookings.html', context)


@login_required
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    from datetime import datetime, timedelta

    # Check if user is admin or staff
    if not request.user.is_staff_member and not request.user.is_admin:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('booking:home')

    # Get statistics
    today = datetime.now().date()
    last_month = today - timedelta(days=30)

    # Calculate stats
    total_bookings = Booking.objects.filter(
        booking_date__gte=last_month,
        booking_date__lte=today
    ).count()

    pending_bookings = Booking.objects.filter(status='pending').count()
    completed_bookings = Booking.objects.filter(status='completed').count()

    # Get recent bookings
    bookings = Booking.objects.all().order_by('-created_at')[:10]

    context = {
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'completed_bookings': completed_bookings,
        'bookings': bookings,
    }

    return render(request, 'booking_management/admin_dashboard.html', context)
