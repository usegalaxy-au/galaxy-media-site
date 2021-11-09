"""Custom form widgets."""

from django.forms.widgets import Input


class ColorInput(Input):
    """Let users pick a color."""

    input_type = 'color'
