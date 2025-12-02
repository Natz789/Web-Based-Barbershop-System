"""
URL configuration for booking_management app
"""
from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('services/', views.services_list, name='services_list'),

    # Booking operations (CRUD)
    path('book/', views.book_appointment, name='book_appointment'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/edit/', views.booking_edit, name='booking_edit'),
    path('booking/<int:booking_id>/cancel/', views.booking_cancel, name='booking_cancel'),

    # Admin dashboard
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
