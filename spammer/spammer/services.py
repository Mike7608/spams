from enum import Enum

NULLABLE = {'null': True, 'blank': True}


class StyleFormMixin:
    """
    Миксин для стилизации формы
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

