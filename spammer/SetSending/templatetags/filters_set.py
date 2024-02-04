from django import template

from SetSending.models import SetSending
from spammer.services import Status
from spammer.settings import INTERVALS
register = template.Library()


@register.filter()
def status_text(pk):
    """
    Процедура возвращает статус рассылки
    """
    status_t = '(нет)'
    sets: SetSending = SetSending.objects.get(id=pk)

    for item in Status.rus_list:
        if item.get('value') == sets.status:
            status_t = item.get('text')
    return status_t


@register.filter()
def interval_text(pk):
    """
    Процедура возвращает период рассылки
    """
    interval_t = '(нет)'
    sets: SetSending = SetSending.objects.get(id=pk)

    for item in INTERVALS:
        if item.get('value') == sets.interval:
            days = ((sets.interval/60)/60)/24
            interval_t = f'1/{int(days)}'
    return interval_t


@register.filter()
def date_start(pk):
    data = '(нет)'
    sets: SetSending = SetSending.objects.get(id=pk)
    data = convert_date(sets.time_start)
    return data


@register.filter()
def date_end(pk):
    data = '(нет)'
    sets: SetSending = SetSending.objects.get(id=pk)
    data = convert_date(sets.time_end)
    return data


def convert_date(value):
    """
    Процедура возвращает дату в формате дд.мм.гггг | чч.мм
    """
    return value.strftime("%d.%m.%Y | %H:%M")


@register.filter()
def color_status(pk):
    """
    Процедура возвращает клаасс цвета Bootstrap для текста
    :param pk:
    :return:
    """
    sets: SetSending = SetSending.objects.get(id=pk)
    status = sets.status
    value = 'text-white'
    if status == Status.Completed:
        value = 'text-secondary'
    if status == Status.Running:
        value = 'text-warning'
    if status == Status.Created:
        value = 'text-success'
    return value
