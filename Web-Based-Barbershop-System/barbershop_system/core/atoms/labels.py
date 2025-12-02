"""
Label Atoms - Basic label and badge components
"""
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class Label:
    """Form label atom"""

    def __init__(self, text, for_field=None, css_class='form-label', required=False):
        self.text = text
        self.for_field = for_field
        self.css_class = css_class
        self.required = required

    def render(self):
        """Render label HTML"""
        for_attr = f'for="{self.for_field}"' if self.for_field else ''
        required_mark = '<span class="text-danger">*</span>' if self.required else ''

        return format_html(
            '<label {} class="{}">{} {}</label>',
            mark_safe(for_attr),
            mark_safe(self.css_class),
            mark_safe(self.text),
            mark_safe(required_mark)
        )

    def __str__(self):
        return str(self.render())


class Badge:
    """Badge atom for status indicators"""

    def __init__(self, text, badge_type='primary', css_class=''):
        self.text = text
        self.badge_type = badge_type
        self.css_class = css_class

    def render(self):
        """Render badge HTML"""
        return format_html(
            '<span class="badge badge-{} {}">{}</span>',
            mark_safe(self.badge_type),
            mark_safe(self.css_class),
            mark_safe(self.text)
        )

    def __str__(self):
        return str(self.render())


class Tag:
    """Tag atom for categorization"""

    def __init__(self, text, removable=False, on_remove=None):
        self.text = text
        self.removable = removable
        self.on_remove = on_remove

    def render(self):
        """Render tag HTML"""
        remove_btn = ''
        if self.removable:
            onclick_attr = f'onclick="{self.on_remove}"' if self.on_remove else ''
            remove_btn = f'<button type="button" class="tag-remove" {onclick_attr}>×</button>'

        return format_html(
            '<span class="tag">{} {}</span>',
            mark_safe(self.text),
            mark_safe(remove_btn)
        )

    def __str__(self):
        return str(self.render())


class StatusBadge(Badge):
    """Specialized badge for booking/payment status"""

    STATUS_COLORS = {
        'pending': 'warning',
        'confirmed': 'info',
        'completed': 'success',
        'cancelled': 'danger',
        'paid': 'success',
        'unpaid': 'warning',
        'refunded': 'secondary'
    }

    def __init__(self, status):
        badge_type = self.STATUS_COLORS.get(status.lower(), 'secondary')
        super().__init__(status.title(), badge_type=badge_type)
