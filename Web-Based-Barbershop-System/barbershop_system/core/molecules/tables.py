"""
Table Molecules - Displaying data in tabular format
"""
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from core.atoms.labels import Badge, StatusBadge
from core.atoms.buttons import Button, IconButton


class Table:
    """Basic table molecule"""

    def __init__(self, headers, rows, css_class='table table-striped'):
        self.headers = headers
        self.rows = rows
        self.css_class = css_class

    def render(self):
        """Render table HTML"""
        header_html = '<tr>'
        for header in self.headers:
            header_html += f'<th>{header}</th>'
        header_html += '</tr>'

        rows_html = ''
        for row in self.rows:
            rows_html += '<tr>'
            for cell in row:
                rows_html += f'<td>{cell}</td>'
            rows_html += '</tr>'

        return format_html(
            '<div class="table-responsive">'
            '<table class="{}">'
            '<thead>{}</thead>'
            '<tbody>{}</tbody>'
            '</table>'
            '</div>',
            mark_safe(self.css_class),
            mark_safe(header_html),
            mark_safe(rows_html)
        )

    def __str__(self):
        return str(self.render())


class BookingTable(Table):
    """Specialized table for displaying bookings"""

    def __init__(self, bookings, show_actions=True):
        self.bookings = bookings
        self.show_actions = show_actions

        headers = ['ID', 'Customer', 'Service', 'Date', 'Time', 'Barber', 'Status']
        if show_actions:
            headers.append('Actions')

        rows = self._build_rows()
        super().__init__(headers, rows, css_class='table table-hover booking-table')

    def _build_rows(self):
        """Build table rows from booking data"""
        rows = []
        for booking in self.bookings:
            status_badge = StatusBadge(booking.get('status', 'pending')).render()

            row = [
                booking.get('id', ''),
                booking.get('customer_name', ''),
                booking.get('service_name', ''),
                booking.get('date', ''),
                booking.get('time', ''),
                booking.get('barber_name', 'Any'),
                status_badge
            ]

            if self.show_actions:
                actions = self._build_actions(booking)
                row.append(actions)

            rows.append(row)

        return rows

    def _build_actions(self, booking):
        """Build action buttons for each booking"""
        booking_id = booking.get('id', '')
        status = booking.get('status', 'pending')

        actions_html = '<div class="btn-group" role="group">'

        # View button
        actions_html += f'''
            <a href="/bookings/{booking_id}" class="btn btn-sm btn-info">
                <i class="fas fa-eye"></i>
            </a>
        '''

        # Edit button (only for pending/confirmed)
        if status in ['pending', 'confirmed']:
            actions_html += f'''
                <a href="/bookings/{booking_id}/edit" class="btn btn-sm btn-primary">
                    <i class="fas fa-edit"></i>
                </a>
            '''

        # Cancel button (only for pending/confirmed)
        if status in ['pending', 'confirmed']:
            actions_html += f'''
                <button type="button" class="btn btn-sm btn-danger"
                        onclick="cancelBooking({booking_id})">
                    <i class="fas fa-times"></i>
                </button>
            '''

        actions_html += '</div>'
        return actions_html


class ServiceTable(Table):
    """Specialized table for displaying services"""

    def __init__(self, services, show_actions=True):
        self.services = services
        self.show_actions = show_actions

        headers = ['Service Name', 'Description', 'Duration', 'Price']
        if show_actions:
            headers.append('Actions')

        rows = self._build_rows()
        super().__init__(headers, rows, css_class='table table-hover service-table')

    def _build_rows(self):
        """Build table rows from service data"""
        rows = []
        for service in self.services:
            row = [
                service.get('name', ''),
                service.get('description', ''),
                f"{service.get('duration', 0)} min",
                f"${service.get('price', 0)}"
            ]

            if self.show_actions:
                actions = self._build_actions(service)
                row.append(actions)

            rows.append(row)

        return rows

    def _build_actions(self, service):
        """Build action buttons for each service"""
        service_id = service.get('id', '')

        actions_html = f'''
            <div class="btn-group" role="group">
                <a href="/services/{service_id}/edit" class="btn btn-sm btn-primary">
                    <i class="fas fa-edit"></i>
                </a>
                <button type="button" class="btn btn-sm btn-danger"
                        onclick="deleteService({service_id})">
                    <i class="fas fa-trash"></i>
                </button>
                <button type="button" class="btn btn-sm btn-success"
                        data-service-id="{service_id}"
                        onclick="bookService({service_id})">
                    Book
                </button>
            </div>
        '''
        return actions_html


class TransactionTable(Table):
    """Specialized table for displaying transactions"""

    def __init__(self, transactions):
        self.transactions = transactions

        headers = ['Transaction ID', 'Date', 'Customer', 'Service', 'Amount', 'Payment Method', 'Status']
        rows = self._build_rows()
        super().__init__(headers, rows, css_class='table table-hover transaction-table')

    def _build_rows(self):
        """Build table rows from transaction data"""
        rows = []
        for transaction in self.transactions:
            status_badge = StatusBadge(transaction.get('status', 'unpaid')).render()

            row = [
                transaction.get('id', ''),
                transaction.get('date', ''),
                transaction.get('customer_name', ''),
                transaction.get('service_name', ''),
                f"${transaction.get('amount', 0)}",
                transaction.get('payment_method', 'N/A'),
                status_badge
            ]

            rows.append(row)

        return rows
