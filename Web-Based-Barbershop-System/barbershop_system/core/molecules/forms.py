"""
Form Molecules - Combining labels and inputs to create form fields
"""
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from core.atoms.labels import Label
from core.atoms.inputs import (
    TextInput, EmailInput, PasswordInput,
    DateInput, TimeInput, SelectInput, TextArea
)


class FormField:
    """Form field molecule combining label and input"""

    def __init__(self, label_text, input_widget, help_text='', error='', required=False):
        self.label_text = label_text
        self.input_widget = input_widget
        self.help_text = help_text
        self.error = error
        self.required = required

    def render(self):
        """Render form field HTML"""
        label = Label(
            self.label_text,
            for_field=self.input_widget.id,
            required=self.required
        ).render()

        input_html = self.input_widget.render()

        help_html = ''
        if self.help_text:
            help_html = f'<small class="form-text text-muted">{self.help_text}</small>'

        error_html = ''
        if self.error:
            error_html = f'<div class="invalid-feedback d-block">{self.error}</div>'

        return format_html(
            '<div class="form-group mb-3">'
            '{}'
            '{}'
            '{}'
            '{}'
            '</div>',
            mark_safe(label),
            mark_safe(input_html),
            mark_safe(help_html),
            mark_safe(error_html)
        )

    def __str__(self):
        return str(self.render())


class LoginForm:
    """Login form molecule"""

    def __init__(self, action='', method='POST', csrf_token=''):
        self.action = action
        self.method = method
        self.csrf_token = csrf_token

    def render(self):
        """Render login form HTML"""
        email_field = FormField(
            'Email',
            EmailInput('email', placeholder='Enter your email', required=True),
            required=True
        ).render()

        password_field = FormField(
            'Password',
            PasswordInput('password', placeholder='Enter your password', required=True),
            required=True
        ).render()

        csrf_html = f'<input type="hidden" name="csrfmiddlewaretoken" value="{self.csrf_token}">' if self.csrf_token else ''

        return format_html(
            '<form action="{}" method="{}" class="login-form">'
            '{}'
            '{}'
            '{}'
            '<button type="submit" class="btn btn-primary w-100">Login</button>'
            '<div class="text-center mt-3">'
            '<a href="/forgot-password" class="text-muted">Forgot Password?</a>'
            '</div>'
            '</form>',
            mark_safe(self.action),
            mark_safe(self.method),
            mark_safe(csrf_html),
            mark_safe(email_field),
            mark_safe(password_field)
        )

    def __str__(self):
        return str(self.render())


class BookingForm:
    """Booking form molecule"""

    def __init__(self, services=None, barbers=None, action='', method='POST', csrf_token=''):
        self.services = services or []
        self.barbers = barbers or []
        self.action = action
        self.method = method
        self.csrf_token = csrf_token

    def render(self):
        """Render booking form HTML"""
        csrf_html = f'<input type="hidden" name="csrfmiddlewaretoken" value="{self.csrf_token}">' if self.csrf_token else ''

        name_field = FormField(
            'Full Name',
            TextInput('customer_name', placeholder='Enter your full name', required=True),
            required=True
        ).render()

        email_field = FormField(
            'Email',
            EmailInput('customer_email', placeholder='Enter your email', required=True),
            required=True
        ).render()

        phone_field = FormField(
            'Phone Number',
            TextInput('customer_phone', placeholder='Enter your phone number', required=True),
            required=True
        ).render()

        service_field = FormField(
            'Service',
            SelectInput('service', self.services, required=True),
            required=True
        ).render()

        barber_field = FormField(
            'Barber',
            SelectInput('barber', self.barbers, required=True),
            help_text='Select your preferred barber',
            required=True
        ).render()

        date_field = FormField(
            'Date',
            DateInput('booking_date', required=True),
            required=True
        ).render()

        time_field = FormField(
            'Time',
            TimeInput('booking_time', required=True),
            required=True
        ).render()

        notes_field = FormField(
            'Additional Notes',
            TextArea('notes', placeholder='Any special requests or notes...', rows=3),
            help_text='Optional: Let us know if you have any special requirements'
        ).render()

        return format_html(
            '<form action="{}" method="{}" class="booking-form">'
            '{}'
            '{}'
            '{}'
            '{}'
            '{}'
            '{}'
            '{}'
            '{}'
            '{}'
            '<button type="submit" class="btn btn-primary btn-lg w-100">Book Appointment</button>'
            '</form>',
            mark_safe(self.action),
            mark_safe(self.method),
            mark_safe(csrf_html),
            mark_safe(name_field),
            mark_safe(email_field),
            mark_safe(phone_field),
            mark_safe(service_field),
            mark_safe(barber_field),
            mark_safe(date_field),
            mark_safe(time_field),
            mark_safe(notes_field)
        )

    def __str__(self):
        return str(self.render())


class ContactForm:
    """Contact form molecule"""

    def __init__(self, action='', method='POST', csrf_token=''):
        self.action = action
        self.method = method
        self.csrf_token = csrf_token

    def render(self):
        """Render contact form HTML"""
        csrf_html = f'<input type="hidden" name="csrfmiddlewaretoken" value="{self.csrf_token}">' if self.csrf_token else ''

        name_field = FormField(
            'Name',
            TextInput('name', placeholder='Your name', required=True),
            required=True
        ).render()

        email_field = FormField(
            'Email',
            EmailInput('email', placeholder='Your email', required=True),
            required=True
        ).render()

        subject_field = FormField(
            'Subject',
            TextInput('subject', placeholder='Subject', required=True),
            required=True
        ).render()

        message_field = FormField(
            'Message',
            TextArea('message', placeholder='Your message...', rows=5, required=True),
            required=True
        ).render()

        return format_html(
            '<form action="{}" method="{}" class="contact-form">'
            '{}'
            '{}'
            '{}'
            '{}'
            '{}'
            '<button type="submit" class="btn btn-primary">Send Message</button>'
            '</form>',
            mark_safe(self.action),
            mark_safe(self.method),
            mark_safe(csrf_html),
            mark_safe(name_field),
            mark_safe(email_field),
            mark_safe(subject_field),
            mark_safe(message_field)
        )

    def __str__(self):
        return str(self.render())
