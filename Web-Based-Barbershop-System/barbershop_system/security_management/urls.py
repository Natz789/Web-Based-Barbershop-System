"""
URL configuration for security_management app
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'security'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='security/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
