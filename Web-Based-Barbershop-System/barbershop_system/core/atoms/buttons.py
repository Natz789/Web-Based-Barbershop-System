"""
Button Atoms - Basic button components
"""
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class Button:
    """Base button atom"""

    def __init__(self, text, button_type='button', css_class='btn-primary',
                 onclick=None, disabled=False, id=None, name=None):
        self.text = text
        self.button_type = button_type
        self.css_class = css_class
        self.onclick = onclick
        self.disabled = disabled
        self.id = id
        self.name = name

    def render(self):
        """Render button HTML"""
        disabled_attr = 'disabled' if self.disabled else ''
        onclick_attr = f'onclick="{self.onclick}"' if self.onclick else ''
        id_attr = f'id="{self.id}"' if self.id else ''
        name_attr = f'name="{self.name}"' if self.name else ''

        return format_html(
            '<button type="{}" class="btn {}" {} {} {} {}>{}</button>',
            mark_safe(self.button_type),
            mark_safe(self.css_class),
            mark_safe(disabled_attr),
            mark_safe(onclick_attr),
            mark_safe(id_attr),
            mark_safe(name_attr),
            mark_safe(self.text)
        )

    def __str__(self):
        return str(self.render())


class IconButton(Button):
    """Button with icon"""

    def __init__(self, text, icon_class, **kwargs):
        super().__init__(text, **kwargs)
        self.icon_class = icon_class

    def render(self):
        """Render icon button HTML"""
        disabled_attr = 'disabled' if self.disabled else ''
        onclick_attr = f'onclick="{self.onclick}"' if self.onclick else ''
        id_attr = f'id="{self.id}"' if self.id else ''
        name_attr = f'name="{self.name}"' if self.name else ''

        return format_html(
            '<button type="{}" class="btn btn-icon {}" {} {} {} {}>'
            '<i class="{}"></i> {}'
            '</button>',
            mark_safe(self.button_type),
            mark_safe(self.css_class),
            mark_safe(disabled_attr),
            mark_safe(onclick_attr),
            mark_safe(id_attr),
            mark_safe(name_attr),
            mark_safe(self.icon_class),
            mark_safe(self.text)
        )


class LinkButton:
    """Link styled as button"""

    def __init__(self, text, href, css_class='btn-link', target='_self'):
        self.text = text
        self.href = href
        self.css_class = css_class
        self.target = target

    def render(self):
        """Render link button HTML"""
        return format_html(
            '<a href="{}" class="btn {}" target="{}">{}</a>',
            mark_safe(self.href),
            mark_safe(self.css_class),
            mark_safe(self.target),
            mark_safe(self.text)
        )

    def __str__(self):
        return str(self.render())
