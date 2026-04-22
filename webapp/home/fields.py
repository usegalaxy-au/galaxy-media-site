"""Custom form fields."""

from django import forms
from django.core.exceptions import ValidationError


class OtherChoiceWidget(forms.MultiWidget):
    """Widget pairing a radio group with a hidden 'Other' text input.

    Reads POST keys ``name`` (radio choice) and ``name_other`` (free-text)
    so that templates can render the two inputs under those conventional names
    rather than the default MultiWidget ``name_0`` / ``name_1`` scheme.
    """

    def __init__(self, choices, min=None, max=None, attrs=None):
        self.choices = choices
        number_attrs = {}
        if min is not None:
            number_attrs['min'] = min
        if max is not None:
            number_attrs['max'] = max
        widgets = [
            forms.RadioSelect(choices=choices),
            forms.NumberInput(attrs=number_attrs or None),
        ]
        super().__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        return [data.get(name), data.get(f'{name}_other')]

    def decompress(self, value):
        """Split a compressed value back into [radio_choice, other_value]."""
        if value is None:
            return [None, None]
        predefined = [str(c[0]) for c in self.choices]
        if str(value) in predefined:
            return [str(value), None]
        return ['0', str(value)]


class OtherChoiceField(forms.MultiValueField):
    """A field for a radio-button group that includes an 'Other' option.

    The 'Other' option is indicated by a sentinel radio value of ``0``.
    When selected, the companion ``name_other`` input is used as the value.
    The final cleaned value is always a float.

    Usage::

        disk_tb = OtherChoiceField(choices=[
            (0.5, '500 GB'),
            (1.0, '1 TB'),
            (2.0, '2 TB'),
        ])
    """

    OTHER_SENTINEL = 0

    def __init__(self, choices, min=None, max=None, **kwargs):
        self.min = min
        self.max = max
        all_choices = list(choices) + [(self.OTHER_SENTINEL, 'Other')]
        widget = OtherChoiceWidget(choices=all_choices, min=min, max=max)
        fields = [
            forms.CharField(required=False),
            forms.CharField(required=False),
        ]
        kwargs.setdefault('require_all_fields', False)
        super().__init__(fields=fields, widget=widget, **kwargs)

    def compress(self, data_list):
        choice = data_list[0] if data_list else None
        other = data_list[1] if len(data_list) > 1 else None

        if not choice:
            raise ValidationError('This field is required.')

        try:
            choice_val = float(choice)
        except (ValueError, TypeError):
            raise ValidationError('Enter a valid value.')

        if choice_val == self.OTHER_SENTINEL:
            if not other:
                raise ValidationError('Please specify a value.')
            try:
                other_val = float(other)
            except (ValueError, TypeError):
                raise ValidationError('Enter a valid number.')
            if self.min is not None and other_val < self.min:
                raise ValidationError(
                    f'Value must be at least {self.min}.')
            if self.max is not None and other_val > self.max:
                raise ValidationError(
                    f'Value must be no more than {self.max}.')
            return other_val

        return choice_val
