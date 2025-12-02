"""
Dashboard Organisms - Complex dashboard components
"""
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from core.molecules.cards import StatsCard
from core.molecules.tables import BookingTable, TransactionTable


class Dashboard:
    """Main dashboard organism"""

    def __init__(self, title='Dashboard', widgets=None):
        self.title = title
        self.widgets = widgets or []

    def render(self):
        """Render dashboard HTML"""
        widgets_html = ''
        for widget in self.widgets:
            widgets_html += str(widget)

        return format_html(
            '<div class="dashboard">'
            '<div class="dashboard-header">'
            '<h2>{}</h2>'
            '</div>'
            '<div class="dashboard-content">{}</div>'
            '</div>',
            mark_safe(self.title),
            mark_safe(widgets_html)
        )

    def __str__(self):
        return str(self.render())


class StatsDashboard:
    """Statistics dashboard organism with multiple stats cards"""

    def __init__(self, stats_data=None):
        self.stats_data = stats_data or {}

    def render(self):
        """Render stats dashboard HTML"""
        stats_html = self._build_stats()

        return format_html(
            '<div class="stats-dashboard">'
            '<div class="row g-4">{}</div>'
            '</div>',
            mark_safe(stats_html)
        )

    def _build_stats(self):
        """Build statistics cards"""
        stats_html = ''

        # Total Bookings
        total_bookings = self.stats_data.get('total_bookings', 0)
        bookings_change = self.stats_data.get('bookings_change', 0)
        stats_html += f'''
            <div class="col-md-6 col-lg-3">
                {StatsCard(
                    'Total Bookings',
                    total_bookings,
                    icon_class='fas fa-calendar-check',
                    change_percent=bookings_change,
                    color='primary'
                ).render()}
            </div>
        '''

        # Total Revenue
        total_revenue = self.stats_data.get('total_revenue', 0)
        revenue_change = self.stats_data.get('revenue_change', 0)
        stats_html += f'''
            <div class="col-md-6 col-lg-3">
                {StatsCard(
                    'Total Revenue',
                    f'${total_revenue}',
                    icon_class='fas fa-dollar-sign',
                    change_percent=revenue_change,
                    color='success'
                ).render()}
            </div>
        '''

        # Active Customers
        active_customers = self.stats_data.get('active_customers', 0)
        customers_change = self.stats_data.get('customers_change', 0)
        stats_html += f'''
            <div class="col-md-6 col-lg-3">
                {StatsCard(
                    'Active Customers',
                    active_customers,
                    icon_class='fas fa-users',
                    change_percent=customers_change,
                    color='info'
                ).render()}
            </div>
        '''

        # Pending Bookings
        pending_bookings = self.stats_data.get('pending_bookings', 0)
        stats_html += f'''
            <div class="col-md-6 col-lg-3">
                {StatsCard(
                    'Pending Bookings',
                    pending_bookings,
                    icon_class='fas fa-clock',
                    color='warning'
                ).render()}
            </div>
        '''

        return stats_html

    def __str__(self):
        return str(self.render())


class BookingsDashboard:
    """Bookings dashboard organism combining stats and booking table"""

    def __init__(self, stats_data=None, bookings=None, title='Bookings Management'):
        self.stats_data = stats_data or {}
        self.bookings = bookings or []
        self.title = title

    def render(self):
        """Render bookings dashboard HTML"""
        stats = StatsDashboard(self.stats_data).render()
        table = BookingTable(self.bookings, show_actions=True).render()

        return format_html(
            '<div class="bookings-dashboard">'
            '<div class="dashboard-header mb-4">'
            '<h2>{}</h2>'
            '</div>'
            '<div class="mb-4">{}</div>'
            '<div class="dashboard-table">'
            '<h4>Recent Bookings</h4>'
            '{}'
            '</div>'
            '</div>',
            mark_safe(self.title),
            mark_safe(stats),
            mark_safe(table)
        )

    def __str__(self):
        return str(self.render())


class RevenueChart:
    """Revenue chart widget organism"""

    def __init__(self, chart_data=None, chart_type='line'):
        self.chart_data = chart_data or {}
        self.chart_type = chart_type

    def render(self):
        """Render revenue chart HTML"""
        # This would integrate with Chart.js or similar library
        return format_html(
            '<div class="card revenue-chart">'
            '<div class="card-header">'
            '<h5>Revenue Overview</h5>'
            '</div>'
            '<div class="card-body">'
            '<canvas id="revenueChart" data-chart-type="{}" '
            'data-chart-data="{}" height="300"></canvas>'
            '</div>'
            '</div>',
            mark_safe(self.chart_type),
            mark_safe(str(self.chart_data))
        )

    def __str__(self):
        return str(self.render())


class ActivityFeed:
    """Activity feed organism showing recent activities"""

    def __init__(self, activities=None):
        self.activities = activities or []

    def render(self):
        """Render activity feed HTML"""
        activities_html = self._build_activities()

        return format_html(
            '<div class="card activity-feed">'
            '<div class="card-header">'
            '<h5>Recent Activity</h5>'
            '</div>'
            '<div class="card-body">'
            '<ul class="list-unstyled activity-list">{}</ul>'
            '</div>'
            '</div>',
            mark_safe(activities_html)
        )

    def _build_activities(self):
        """Build activity items"""
        activities_html = ''
        for activity in self.activities:
            icon = activity.get('icon', 'fas fa-circle')
            text = activity.get('text', '')
            time = activity.get('time', '')
            activity_type = activity.get('type', 'default')

            activities_html += f'''
                <li class="activity-item activity-{activity_type}">
                    <div class="activity-icon">
                        <i class="{icon}"></i>
                    </div>
                    <div class="activity-content">
                        <p class="activity-text">{text}</p>
                        <small class="activity-time text-muted">{time}</small>
                    </div>
                </li>
            '''

        return activities_html

    def __str__(self):
        return str(self.render())
