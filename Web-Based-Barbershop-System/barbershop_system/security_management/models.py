from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Extended user model with role-based access"""

    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('barber', 'Barber'),
        ('staff', 'Staff'),
        ('admin', 'Administrator'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_barber(self):
        return self.role == 'barber'

    @property
    def is_staff_member(self):
        return self.role in ['staff', 'admin']

    @property
    def is_admin(self):
        return self.role == 'admin'


class StaffProfile(models.Model):
    """Additional profile information for staff/barbers"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)

    # Working hours
    monday_start = models.TimeField(null=True, blank=True)
    monday_end = models.TimeField(null=True, blank=True)
    tuesday_start = models.TimeField(null=True, blank=True)
    tuesday_end = models.TimeField(null=True, blank=True)
    wednesday_start = models.TimeField(null=True, blank=True)
    wednesday_end = models.TimeField(null=True, blank=True)
    thursday_start = models.TimeField(null=True, blank=True)
    thursday_end = models.TimeField(null=True, blank=True)
    friday_start = models.TimeField(null=True, blank=True)
    friday_end = models.TimeField(null=True, blank=True)
    saturday_start = models.TimeField(null=True, blank=True)
    saturday_end = models.TimeField(null=True, blank=True)
    sunday_start = models.TimeField(null=True, blank=True)
    sunday_end = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staff_profiles'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"

    def update_rating(self, new_rating):
        """Update barber rating with new review"""
        total = (self.rating * self.total_reviews) + new_rating
        self.total_reviews += 1
        self.rating = total / self.total_reviews
        self.save()


class LoginAttempt(models.Model):
    """Track login attempts for security"""

    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        db_table = 'login_attempts'
        ordering = ['-timestamp']

    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"{self.username} - {status} at {self.timestamp}"
