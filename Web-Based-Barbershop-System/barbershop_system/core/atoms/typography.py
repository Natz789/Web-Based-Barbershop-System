"""
Typography Atoms - Basic text components
"""
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class Heading:
    """Heading atom (h1-h6)"""

    def __init__(self, text, level=1, css_class=''):
        self.text = text
        self.level = min(max(level, 1), 6)  # Clamp between 1-6
        self.css_class = css_class

    def render(self):
        """Render heading HTML"""
        tag = f'h{self.level}'
        return format_html(
            '<{} class="{}">{}</{}>',
            mark_safe(tag),
            mark_safe(self.css_class),
            mark_safe(self.text),
            mark_safe(tag)
        )

    def __str__(self):
        return str(self.render())


class Paragraph:
    """Paragraph atom"""

    def __init__(self, text, css_class=''):
        self.text = text
        self.css_class = css_class

    def render(self):
        """Render paragraph HTML"""
        return format_html(
            '<p class="{}">{}</p>',
            mark_safe(self.css_class),
            mark_safe(self.text)
        )

    def __str__(self):
        return str(self.render())


class Span:
    """Span atom for inline text"""

    def __init__(self, text, css_class=''):
        self.text = text
        self.css_class = css_class

    def render(self):
        """Render span HTML"""
        return format_html(
            '<span class="{}">{}</span>',
            mark_safe(self.css_class),
            mark_safe(self.text)
        )

    def __str__(self):
        return str(self.render())
