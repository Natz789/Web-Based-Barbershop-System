"""
Card Molecules - Combining atoms to create card components
"""
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from core.atoms.buttons import Button
from core.atoms.labels import Badge


class Card:
    """Basic card molecule"""

    def __init__(self, title='', content='', footer='', css_class='card'):
        self.title = title
        self.content = content
        self.footer = footer
        self.css_class = css_class

    def render(self):
        """Render card HTML"""
        title_html = f'<div class="card-header"><h5>{self.title}</h5></div>' if self.title else ''
        footer_html = f'<div class="card-footer">{self.footer}</div>' if self.footer else ''

        return format_html(
            '<div class="{}">'
            '{}'
            '<div class="card-body">{}</div>'
            '{}'
            '</div>',
            mark_safe(self.css_class),
            mark_safe(title_html),
            mark_safe(self.content),
            mark_safe(footer_html)
        )

    def __str__(self):
        return str(self.render())


class ServiceCard(Card):
    """Service card showing barbershop services"""

    def __init__(self, service_name, description, price, duration, image_url=None):
        self.service_name = service_name
        self.description = description
        self.price = price
        self.duration = duration
        self.image_url = image_url

        content = self._build_content()
        super().__init__(title=service_name, content=content, css_class='card service-card')

    def _build_content(self):
        """Build service card content"""
        image_html = ''
        if self.image_url:
            image_html = f'<img src="{self.image_url}" class="card-img-top" alt="{self.service_name}">'

        return f'''
            {image_html}
            <p class="service-description">{self.description}</p>
            <div class="service-details">
                <span class="service-price">${self.price}</span>
                <span class="service-duration">{self.duration} min</span>
            </div>
            <button type="button" class="btn btn-primary btn-block book-service" data-service="{self.service_name}">
                Book Now
            </button>
        '''


class BookingCard(Card):
    """Booking card showing appointment details"""

    def __init__(self, booking_id, customer_name, service_name, date, time, status, barber_name=''):
        self.booking_id = booking_id
        self.customer_name = customer_name
        self.service_name = service_name
        self.date = date
        self.time = time
        self.status = status
        self.barber_name = barber_name

        title = f'Booking #{booking_id}'
        content = self._build_content()
        super().__init__(title=title, content=content, css_class='card booking-card')

    def _build_content(self):
        """Build booking card content"""
        from core.atoms.labels import StatusBadge

        status_badge = StatusBadge(self.status).render()
        barber_html = f'<p><strong>Barber:</strong> {self.barber_name}</p>' if self.barber_name else ''

        return f'''
            <div class="booking-details">
                <p><strong>Customer:</strong> {self.customer_name}</p>
                <p><strong>Service:</strong> {self.service_name}</p>
                <p><strong>Date:</strong> {self.date}</p>
                <p><strong>Time:</strong> {self.time}</p>
                {barber_html}
                <p><strong>Status:</strong> {status_badge}</p>
            </div>
        '''


class StatsCard(Card):
    """Statistics card for dashboard"""

    def __init__(self, title, value, icon_class='', change_percent=None, color='primary'):
        self.value = value
        self.icon_class = icon_class
        self.change_percent = change_percent
        self.color = color

        content = self._build_content()
        super().__init__(title=title, content=content, css_class=f'card stats-card stats-{color}')

    def _build_content(self):
        """Build stats card content"""
        icon_html = f'<i class="{self.icon_class} stats-icon"></i>' if self.icon_class else ''

        change_html = ''
        if self.change_percent is not None:
            change_class = 'positive' if self.change_percent > 0 else 'negative'
            change_symbol = '+' if self.change_percent > 0 else ''
            change_html = f'''
                <span class="stats-change {change_class}">
                    {change_symbol}{self.change_percent}%
                </span>
            '''

        return f'''
            <div class="stats-content">
                {icon_html}
                <div class="stats-info">
                    <h2 class="stats-value">{self.value}</h2>
                    {change_html}
                </div>
            </div>
        '''
