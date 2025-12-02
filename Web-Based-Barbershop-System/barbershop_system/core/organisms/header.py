"""
Header Organism - Main page header component
"""
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from core.organisms.navigation import Navigation


class Header:
    """Main header organism combining navigation and branding"""

    def __init__(self, brand_name='Barbershop System', brand_logo=None,
                 nav_items=None, user=None, current_path='', show_hero=False,
                 hero_title='', hero_subtitle=''):
        self.brand_name = brand_name
        self.brand_logo = brand_logo
        self.nav_items = nav_items or []
        self.user = user
        self.current_path = current_path
        self.show_hero = show_hero
        self.hero_title = hero_title
        self.hero_subtitle = hero_subtitle

    def render(self):
        """Render header HTML"""
        navigation = Navigation(
            brand_name=self.brand_name,
            brand_logo=self.brand_logo,
            nav_items=self.nav_items,
            user=self.user,
            current_path=self.current_path
        ).render()

        hero_html = ''
        if self.show_hero:
            hero_html = self._build_hero()

        return format_html(
            '<header class="main-header">'
            '{}'
            '{}'
            '</header>',
            mark_safe(navigation),
            mark_safe(hero_html)
        )

    def _build_hero(self):
        """Build hero section"""
        return f'''
            <div class="hero-section">
                <div class="container">
                    <div class="hero-content text-center">
                        <h1 class="hero-title">{self.hero_title}</h1>
                        <p class="hero-subtitle">{self.hero_subtitle}</p>
                        <div class="hero-actions mt-4">
                            <a href="/book" class="btn btn-primary btn-lg">Book Appointment</a>
                            <a href="/services" class="btn btn-outline-light btn-lg ms-2">View Services</a>
                        </div>
                    </div>
                </div>
            </div>
        '''

    def __str__(self):
        return str(self.render())


class PageHeader:
    """Simple page header with title and actions"""

    def __init__(self, title, subtitle='', actions=None, breadcrumbs=None):
        self.title = title
        self.subtitle = subtitle
        self.actions = actions or []
        self.breadcrumbs = breadcrumbs

    def render(self):
        """Render page header HTML"""
        breadcrumb_html = ''
        if self.breadcrumbs:
            from core.organisms.navigation import Breadcrumb
            breadcrumb_html = Breadcrumb(self.breadcrumbs).render()

        subtitle_html = f'<p class="page-subtitle text-muted">{self.subtitle}</p>' if self.subtitle else ''

        actions_html = ''
        if self.actions:
            actions_html = '<div class="page-actions">'
            for action in self.actions:
                actions_html += str(action)
            actions_html += '</div>'

        return format_html(
            '<div class="page-header">'
            '{}'
            '<div class="d-flex justify-content-between align-items-center">'
            '<div>'
            '<h1 class="page-title">{}</h1>'
            '{}'
            '</div>'
            '{}'
            '</div>'
            '</div>',
            mark_safe(breadcrumb_html),
            mark_safe(self.title),
            mark_safe(subtitle_html),
            mark_safe(actions_html)
        )

    def __str__(self):
        return str(self.render())
