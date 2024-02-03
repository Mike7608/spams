from django import template
from spammer.services import Status
from spammer.settings import INTERVALS
register = template.Library()


@register.filter()
def status_text(status):
    """
    Процедура возвращает строку названия Статуса
    """
    status_t = '(нет)'
    for item in Status.rus_list:
        if item.get('value') == status:
            status_t = item.get('text')

    return status_t


@register.filter()
def interval_text(interval):
    """
    Процедура возвращает строку названия Статуса
    """
    interval_t = '(нет)'
    for item in INTERVALS:
        if item.get('value') == interval:
            interval_t = item.get('text')
    return interval_t