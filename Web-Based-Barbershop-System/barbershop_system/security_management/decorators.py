"""
Security decorators for role-based access control
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    """Decorator to check if user has required role"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'You must be logged in to access this page.')
                return redirect('login')

            if request.user.role not in roles:
                messages.error(request, 'You do not have permission to access this page.')
                raise PermissionDenied

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def admin_required(view_func):
    """Decorator to check if user is admin"""
    return role_required('admin')(view_func)


def staff_required(view_func):
    """Decorator to check if user is staff or admin"""
    return role_required('admin', 'staff')(view_func)


def barber_required(view_func):
    """Decorator to check if user is barber"""
    return role_required('barber', 'admin')(view_func)


def customer_required(view_func):
    """Decorator to check if user is customer"""
    return role_required('customer')(view_func)
