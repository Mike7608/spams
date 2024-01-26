from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def mediapath(file_name):
    return f"{settings.MEDIA_URL}{file_name}"
