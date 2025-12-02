"""
URL configuration for booking_management app
"""
from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_list, name='services_list'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
