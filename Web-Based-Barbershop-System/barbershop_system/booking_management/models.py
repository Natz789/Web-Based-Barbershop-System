from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone


class Service(models.Model):
    """Barbershop services"""

    name = models.CharField(max_length=200)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Duration in minutes"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'services'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - ${self.price}"


class Customer(models.Model):
    """Customer information"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_profile',
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=17)
    preferences = models.TextField(blank=True, help_text="Customer preferences or notes")
    total_bookings = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Booking(models.Model):
    """Booking/Appointment model"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='bookings')
    barber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='barber_bookings',
        limit_choices_to={'role': 'barber'}
    )
    booking_date = models.DateField()
    booking_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'bookings'
        ordering = ['-booking_date', '-booking_time']
        indexes = [
            models.Index(fields=['booking_date', 'booking_time']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Booking #{self.id} - {self.customer.full_name} - {self.booking_date}"

    def save(self, *args, **kwargs):
        # Auto-calculate end time based on service duration
        if not self.end_time and self.service:
            from datetime import datetime, timedelta
            start_datetime = datetime.combine(self.booking_date, self.booking_time)
            end_datetime = start_datetime + timedelta(minutes=self.service.duration_minutes)
            self.end_time = end_datetime.time()
        super().save(*args, **kwargs)

    def confirm(self):
        """Confirm the booking"""
        self.status = 'confirmed'
        self.confirmed_at = timezone.now()
        self.save()

    def complete(self):
        """Mark booking as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

    def cancel(self, reason=''):
        """Cancel the booking"""
        self.status = 'cancelled'
        self.cancellation_reason = reason
        self.save()

    @property
    def is_upcoming(self):
        """Check if booking is upcoming"""
        from datetime import datetime
        booking_datetime = datetime.combine(self.booking_date, self.booking_time)
        return booking_datetime > datetime.now() and self.status in ['pending', 'confirmed']

    @property
    def can_cancel(self):
        """Check if booking can be cancelled"""
        return self.status in ['pending', 'confirmed'] and self.is_upcoming


class Review(models.Model):
    """Customer reviews for completed bookings"""

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    barber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='barber_reviews'
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Rating from 1 to 5"
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.customer.full_name} - {self.rating} stars"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update barber rating
        if hasattr(self.barber, 'staff_profile'):
            self.barber.staff_profile.update_rating(self.rating)
