from django import template
from Logs.models import Logs
from clients.models import Client
from message.models import Message
from SetSending.models import SetSending


register = template.Library()

@register.simple_tag
def get_current_user(user):
    return user


@register.simple_tag
def count_row_clients(user):
    if user:
        value: Client = Client.objects.filter(user_id=user.pk)
    return len(value)


@register.simple_tag
def count_row_message(user):
    if user:
        value: Message = Message.objects.filter(user_id=user.pk)
    return len(value)


@register.simple_tag
def count_row_setsending(user):
    if user:
        value: SetSending = SetSending.objects.filter(user_id=user.pk)
    return len(value)


@register.simple_tag
def count_row_logs():
    return Logs.objects.count()
