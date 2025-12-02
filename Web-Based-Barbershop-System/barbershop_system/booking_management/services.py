"""
Business logic layer for booking management
"""
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Booking, Service, Customer, Review


class BookingService:
    """Service layer for booking operations"""

    @staticmethod
    def create_booking(customer_data, booking_data):
        """Create a new booking with customer information"""
        # Get or create customer
        customer, created = Customer.objects.get_or_create(
            email=customer_data['email'],
            defaults={
                'first_name': customer_data['first_name'],
                'last_name': customer_data['last_name'],
                'phone_number': customer_data['phone_number']
            }
        )

        # Create booking
        booking = Booking.objects.create(
            customer=customer,
            service_id=booking_data['service_id'],
            barber_id=booking_data.get('barber_id'),
            booking_date=booking_data['booking_date'],
            booking_time=booking_data['booking_time'],
            notes=booking_data.get('notes', '')
        )

        customer.total_bookings += 1
        customer.save()

        return booking

    @staticmethod
    def get_available_time_slots(date, service_id, barber_id=None):
        """Get available time slots for a given date and service"""
        service = Service.objects.get(id=service_id)
        duration = service.duration_minutes

        # Business hours (can be configured)
        start_hour = 9
        end_hour = 18

        # Generate all possible time slots
        slots = []
        current_time = datetime.combine(date, datetime.min.time()).replace(hour=start_hour)
        end_time = datetime.combine(date, datetime.min.time()).replace(hour=end_hour)

        while current_time < end_time:
            slots.append(current_time.time())
            current_time += timedelta(minutes=30)  # 30-minute intervals

        # Get existing bookings for the date
        query = Q(booking_date=date, status__in=['pending', 'confirmed'])
        if barber_id:
            query &= Q(barber_id=barber_id)

        existing_bookings = Booking.objects.filter(query)

        # Remove occupied slots
        available_slots = []
        for slot in slots:
            is_available = True
            for booking in existing_bookings:
                if booking.booking_time <= slot < booking.end_time:
                    is_available = False
                    break
            if is_available:
                available_slots.append(slot)

        return available_slots

    @staticmethod
    def get_upcoming_bookings(customer=None, barber=None, limit=None):
        """Get upcoming bookings"""
        today = timezone.now().date()
        query = Q(booking_date__gte=today, status__in=['pending', 'confirmed'])

        if customer:
            query &= Q(customer=customer)
        if barber:
            query &= Q(barber=barber)

        bookings = Booking.objects.filter(query).order_by('booking_date', 'booking_time')

        if limit:
            bookings = bookings[:limit]

        return bookings

    @staticmethod
    def get_booking_statistics(start_date=None, end_date=None):
        """Get booking statistics for dashboard"""
        query = Q()
        if start_date:
            query &= Q(booking_date__gte=start_date)
        if end_date:
            query &= Q(booking_date__lte=end_date)

        bookings = Booking.objects.filter(query)

        stats = {
            'total_bookings': bookings.count(),
            'pending_bookings': bookings.filter(status='pending').count(),
            'confirmed_bookings': bookings.filter(status='confirmed').count(),
            'completed_bookings': bookings.filter(status='completed').count(),
            'cancelled_bookings': bookings.filter(status='cancelled').count(),
            'revenue': bookings.filter(
                status='completed'
            ).aggregate(
                total=Sum('service__price')
            )['total'] or 0
        }

        return stats

    @staticmethod
    def cancel_booking(booking_id, reason=''):
        """Cancel a booking"""
        booking = Booking.objects.get(id=booking_id)
        if booking.can_cancel:
            booking.cancel(reason)
            return True
        return False


class ServiceManagement:
    """Service management operations"""

    @staticmethod
    def get_active_services(category=None):
        """Get active services"""
        query = Q(is_active=True)
        if category:
            query &= Q(category=category)

        return Service.objects.filter(query).order_by('name')

    @staticmethod
    def get_popular_services(limit=5):
        """Get most popular services"""
        return Service.objects.filter(
            is_active=True
        ).annotate(
            booking_count=Count('bookings')
        ).order_by('-booking_count')[:limit]


class ReviewService:
    """Review management operations"""

    @staticmethod
    def create_review(booking_id, rating, comment=''):
        """Create a review for a completed booking"""
        booking = Booking.objects.get(id=booking_id)

        if booking.status != 'completed':
            raise ValueError("Can only review completed bookings")

        if hasattr(booking, 'review'):
            raise ValueError("Booking already has a review")

        review = Review.objects.create(
            booking=booking,
            customer=booking.customer,
            barber=booking.barber,
            rating=rating,
            comment=comment
        )

        return review

    @staticmethod
    def get_barber_reviews(barber_id, limit=None):
        """Get reviews for a barber"""
        reviews = Review.objects.filter(barber_id=barber_id).order_by('-created_at')
        if limit:
            reviews = reviews[:limit]
        return reviews
