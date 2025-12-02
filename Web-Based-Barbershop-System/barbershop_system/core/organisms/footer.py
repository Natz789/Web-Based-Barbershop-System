"""
Footer Organism - Main page footer component
"""
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from datetime import datetime


class Footer:
    """Main footer organism"""

    def __init__(self, brand_name='Barbershop System', social_links=None,
                 contact_info=None, quick_links=None):
        self.brand_name = brand_name
        self.social_links = social_links or []
        self.contact_info = contact_info or {}
        self.quick_links = quick_links or []
        self.current_year = datetime.now().year

    def render(self):
        """Render footer HTML"""
        about_html = self._build_about_section()
        quick_links_html = self._build_quick_links()
        contact_html = self._build_contact_section()
        social_html = self._build_social_links()
        copyright_html = self._build_copyright()

        return format_html(
            '<footer class="main-footer">'
            '<div class="container">'
            '<div class="row">'
            '<div class="col-md-4">{}</div>'
            '<div class="col-md-3">{}</div>'
            '<div class="col-md-3">{}</div>'
            '<div class="col-md-2">{}</div>'
            '</div>'
            '<hr class="footer-divider">'
            '{}'
            '</div>'
            '</footer>',
            mark_safe(about_html),
            mark_safe(quick_links_html),
            mark_safe(contact_html),
            mark_safe(social_html),
            mark_safe(copyright_html)
        )

    def _build_about_section(self):
        """Build about section"""
        return f'''
            <div class="footer-section">
                <h5>{self.brand_name}</h5>
                <p class="text-muted">
                    Your trusted barbershop for professional grooming services.
                    Quality cuts, friendly service, and a great experience every time.
                </p>
            </div>
        '''

    def _build_quick_links(self):
        """Build quick links section"""
        links_html = ''
        for link in self.quick_links:
            url = link.get('url', '#')
            label = link.get('label', '')
            links_html += f'<li><a href="{url}" class="footer-link">{label}</a></li>'

        return f'''
            <div class="footer-section">
                <h5>Quick Links</h5>
                <ul class="footer-links list-unstyled">
                    {links_html}
                </ul>
            </div>
        '''

    def _build_contact_section(self):
        """Build contact information section"""
        phone = self.contact_info.get('phone', '')
        email = self.contact_info.get('email', '')
        address = self.contact_info.get('address', '')

        phone_html = f'<p><i class="fas fa-phone"></i> {phone}</p>' if phone else ''
        email_html = f'<p><i class="fas fa-envelope"></i> {email}</p>' if email else ''
        address_html = f'<p><i class="fas fa-map-marker-alt"></i> {address}</p>' if address else ''

        return f'''
            <div class="footer-section">
                <h5>Contact Us</h5>
                <div class="footer-contact">
                    {phone_html}
                    {email_html}
                    {address_html}
                </div>
            </div>
        '''

    def _build_social_links(self):
        """Build social media links"""
        links_html = ''
        for link in self.social_links:
            platform = link.get('platform', '')
            url = link.get('url', '#')
            icon = link.get('icon', 'fas fa-link')

            links_html += f'''
                <a href="{url}" class="social-link" target="_blank" rel="noopener"
                   aria-label="{platform}">
                    <i class="{icon}"></i>
                </a>
            '''

        return f'''
            <div class="footer-section">
                <h5>Follow Us</h5>
                <div class="social-links">
                    {links_html}
                </div>
            </div>
        '''

    def _build_copyright(self):
        """Build copyright section"""
        return f'''
            <div class="footer-copyright text-center">
                <p class="mb-0">
                    &copy; {self.current_year} {self.brand_name}. All rights reserved.
                </p>
            </div>
        '''

    def __str__(self):
        return str(self.render())


class SimpleFooter:
    """Simplified footer for admin/dashboard pages"""

    def __init__(self, brand_name='Barbershop System'):
        self.brand_name = brand_name
        self.current_year = datetime.now().year

    def render(self):
        """Render simple footer HTML"""
        return format_html(
            '<footer class="simple-footer">'
            '<div class="container">'
            '<div class="text-center py-3">'
            '<p class="mb-0 text-muted">'
            '&copy; {} {}. All rights reserved.'
            '</p>'
            '</div>'
            '</div>'
            '</footer>',
            self.current_year,
            mark_safe(self.brand_name)
        )

    def __str__(self):
        return str(self.render())
