"""
Input Atoms - Basic form input components
"""
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class BaseInput:
    """Base input atom"""

    def __init__(self, name, input_type='text', placeholder='', value='',
                 required=False, disabled=False, css_class='form-control',
                 id=None, autocomplete=None):
        self.name = name
        self.input_type = input_type
        self.placeholder = placeholder
        self.value = value
        self.required = required
        self.disabled = disabled
        self.css_class = css_class
        self.id = id or name
        self.autocomplete = autocomplete

    def render(self):
        """Render input HTML"""
        required_attr = 'required' if self.required else ''
        disabled_attr = 'disabled' if self.disabled else ''
        autocomplete_attr = f'autocomplete="{self.autocomplete}"' if self.autocomplete else ''

        return format_html(
            '<input type="{}" name="{}" id="{}" class="{}" '
            'placeholder="{}" value="{}" {} {} {} />',
            mark_safe(self.input_type),
            mark_safe(self.name),
            mark_safe(self.id),
            mark_safe(self.css_class),
            mark_safe(self.placeholder),
            mark_safe(self.value),
            mark_safe(required_attr),
            mark_safe(disabled_attr),
            mark_safe(autocomplete_attr)
        )

    def __str__(self):
        return str(self.render())


class TextInput(BaseInput):
    """Text input field"""

    def __init__(self, name, **kwargs):
        super().__init__(name, input_type='text', **kwargs)


class EmailInput(BaseInput):
    """Email input field"""

    def __init__(self, name, **kwargs):
        kwargs.setdefault('autocomplete', 'email')
        super().__init__(name, input_type='email', **kwargs)


class PasswordInput(BaseInput):
    """Password input field"""

    def __init__(self, name, **kwargs):
        kwargs.setdefault('autocomplete', 'current-password')
        super().__init__(name, input_type='password', **kwargs)


class DateInput(BaseInput):
    """Date input field"""

    def __init__(self, name, **kwargs):
        super().__init__(name, input_type='date', **kwargs)


class TimeInput(BaseInput):
    """Time input field"""

    def __init__(self, name, **kwargs):
        super().__init__(name, input_type='time', **kwargs)


class NumberInput(BaseInput):
    """Number input field"""

    def __init__(self, name, min_value=None, max_value=None, step=None, **kwargs):
        super().__init__(name, input_type='number', **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step

    def render(self):
        """Render number input HTML"""
        required_attr = 'required' if self.required else ''
        disabled_attr = 'disabled' if self.disabled else ''
        min_attr = f'min="{self.min_value}"' if self.min_value is not None else ''
        max_attr = f'max="{self.max_value}"' if self.max_value is not None else ''
        step_attr = f'step="{self.step}"' if self.step is not None else ''

        return format_html(
            '<input type="number" name="{}" id="{}" class="{}" '
            'placeholder="{}" value="{}" {} {} {} {} {} />',
            mark_safe(self.name),
            mark_safe(self.id),
            mark_safe(self.css_class),
            mark_safe(self.placeholder),
            mark_safe(self.value),
            mark_safe(required_attr),
            mark_safe(disabled_attr),
            mark_safe(min_attr),
            mark_safe(max_attr),
            mark_safe(step_attr)
        )


class TextArea:
    """Textarea field"""

    def __init__(self, name, placeholder='', value='', rows=4,
                 required=False, disabled=False, css_class='form-control', id=None):
        self.name = name
        self.placeholder = placeholder
        self.value = value
        self.rows = rows
        self.required = required
        self.disabled = disabled
        self.css_class = css_class
        self.id = id or name

    def render(self):
        """Render textarea HTML"""
        required_attr = 'required' if self.required else ''
        disabled_attr = 'disabled' if self.disabled else ''

        return format_html(
            '<textarea name="{}" id="{}" class="{}" placeholder="{}" '
            'rows="{}" {} {}>{}</textarea>',
            mark_safe(self.name),
            mark_safe(self.id),
            mark_safe(self.css_class),
            mark_safe(self.placeholder),
            self.rows,
            mark_safe(required_attr),
            mark_safe(disabled_attr),
            mark_safe(self.value)
        )

    def __str__(self):
        return str(self.render())


class SelectInput:
    """Select dropdown field"""

    def __init__(self, name, options, selected='', required=False,
                 disabled=False, css_class='form-select', id=None):
        self.name = name
        self.options = options  # List of tuples (value, label)
        self.selected = selected
        self.required = required
        self.disabled = disabled
        self.css_class = css_class
        self.id = id or name

    def render(self):
        """Render select HTML"""
        required_attr = 'required' if self.required else ''
        disabled_attr = 'disabled' if self.disabled else ''

        options_html = ''
        for value, label in self.options:
            selected_attr = 'selected' if str(value) == str(self.selected) else ''
            options_html += f'<option value="{value}" {selected_attr}>{label}</option>'

        return format_html(
            '<select name="{}" id="{}" class="{}" {} {}>{}</select>',
            mark_safe(self.name),
            mark_safe(self.id),
            mark_safe(self.css_class),
            mark_safe(required_attr),
            mark_safe(disabled_attr),
            mark_safe(options_html)
        )

    def __str__(self):
        return str(self.render())
