from django import template
from clients.models import Client
from message.models import Message

register = template.Library()


@register.simple_tag
def count_row_clients():
    return Client.objects.count()


@register.simple_tag
def count_row_message():
    return Message.objects.count()