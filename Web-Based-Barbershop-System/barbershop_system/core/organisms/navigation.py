"""
Navigation Organisms - Complex navigation components
"""
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class Navigation:
    """Main navigation organism"""

    def __init__(self, brand_name='Barbershop', brand_logo=None, nav_items=None,
                 user=None, current_path=''):
        self.brand_name = brand_name
        self.brand_logo = brand_logo
        self.nav_items = nav_items or []
        self.user = user
        self.current_path = current_path

    def render(self):
        """Render navigation HTML"""
        brand_html = self._build_brand()
        nav_items_html = self._build_nav_items()
        user_menu_html = self._build_user_menu()

        return format_html(
            '<nav class="navbar navbar-expand-lg navbar-dark bg-dark">'
            '<div class="container-fluid">'
            '{}'
            '<button class="navbar-toggler" type="button" data-bs-toggle="collapse" '
            'data-bs-target="#navbarNav" aria-controls="navbarNav" '
            'aria-expanded="false" aria-label="Toggle navigation">'
            '<span class="navbar-toggler-icon"></span>'
            '</button>'
            '<div class="collapse navbar-collapse" id="navbarNav">'
            '<ul class="navbar-nav me-auto mb-2 mb-lg-0">{}</ul>'
            '{}'
            '</div>'
            '</div>'
            '</nav>',
            mark_safe(brand_html),
            mark_safe(nav_items_html),
            mark_safe(user_menu_html)
        )

    def _build_brand(self):
        """Build brand section"""
        if self.brand_logo:
            return f'''
                <a class="navbar-brand" href="/">
                    <img src="{self.brand_logo}" alt="{self.brand_name}" height="30">
                </a>
            '''
        return f'<a class="navbar-brand" href="/">{self.brand_name}</a>'

    def _build_nav_items(self):
        """Build navigation items"""
        items_html = ''
        for item in self.nav_items:
            url = item.get('url', '#')
            label = item.get('label', '')
            active = 'active' if url == self.current_path else ''

            items_html += f'''
                <li class="nav-item">
                    <a class="nav-link {active}" href="{url}">{label}</a>
                </li>
            '''
        return items_html

    def _build_user_menu(self):
        """Build user menu dropdown"""
        if not self.user:
            return '''
                <div class="d-flex">
                    <a href="/login" class="btn btn-outline-light me-2">Login</a>
                    <a href="/register" class="btn btn-primary">Register</a>
                </div>
            '''

        username = getattr(self.user, 'username', 'User')
        user_role = getattr(self.user, 'role', 'customer')

        return f'''
            <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button"
                        id="userMenuDropdown" data-bs-toggle="dropdown"
                        aria-expanded="false">
                    <i class="fas fa-user"></i> {username}
                </button>
                <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userMenuDropdown">
                    <li><a class="dropdown-item" href="/profile">
                        <i class="fas fa-user-circle"></i> Profile
                    </a></li>
                    <li><a class="dropdown-item" href="/my-bookings">
                        <i class="fas fa-calendar"></i> My Bookings
                    </a></li>
                    {self._build_admin_link(user_role)}
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="/logout">
                        <i class="fas fa-sign-out-alt"></i> Logout
                    </a></li>
                </ul>
            </div>
        '''

    def _build_admin_link(self, user_role):
        """Build admin link if user has admin role"""
        if user_role in ['admin', 'staff']:
            return '''
                <li><a class="dropdown-item" href="/admin/dashboard">
                    <i class="fas fa-tachometer-alt"></i> Admin Dashboard
                </a></li>
            '''
        return ''

    def __str__(self):
        return str(self.render())


class Sidebar:
    """Sidebar navigation organism for admin/dashboard"""

    def __init__(self, items=None, active_item=''):
        self.items = items or []
        self.active_item = active_item

    def render(self):
        """Render sidebar HTML"""
        items_html = self._build_items()

        return format_html(
            '<div class="sidebar">'
            '<div class="sidebar-header">'
            '<h4>Dashboard</h4>'
            '</div>'
            '<nav class="sidebar-nav">'
            '<ul class="nav flex-column">{}</ul>'
            '</nav>'
            '</div>',
            mark_safe(items_html)
        )

    def _build_items(self):
        """Build sidebar items"""
        items_html = ''
        for item in self.items:
            url = item.get('url', '#')
            label = item.get('label', '')
            icon = item.get('icon', 'fas fa-circle')
            badge = item.get('badge', None)
            active = 'active' if label == self.active_item else ''

            badge_html = ''
            if badge:
                badge_html = f'<span class="badge bg-{badge.get("color", "primary")}">{badge.get("text", "")}</span>'

            items_html += f'''
                <li class="nav-item">
                    <a class="nav-link {active}" href="{url}">
                        <i class="{icon}"></i>
                        <span>{label}</span>
                        {badge_html}
                    </a>
                </li>
            '''
        return items_html

    def __str__(self):
        return str(self.render())


class Breadcrumb:
    """Breadcrumb navigation organism"""

    def __init__(self, items):
        self.items = items  # List of tuples (label, url)

    def render(self):
        """Render breadcrumb HTML"""
        items_html = ''
        total_items = len(self.items)

        for i, (label, url) in enumerate(self.items):
            is_last = i == total_items - 1

            if is_last:
                items_html += f'<li class="breadcrumb-item active" aria-current="page">{label}</li>'
            else:
                items_html += f'<li class="breadcrumb-item"><a href="{url}">{label}</a></li>'

        return format_html(
            '<nav aria-label="breadcrumb">'
            '<ol class="breadcrumb">{}</ol>'
            '</nav>',
            mark_safe(items_html)
        )

    def __str__(self):
        return str(self.render())
