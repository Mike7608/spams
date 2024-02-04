from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from spammer.services import DateTimeNow
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DeleteView
from SetSending.models import SetSending
from clients.models import Client
from message.models import Message
from spammer.services import JobService, Status
from spammer.settings import INTERVALS
from datetime import datetime, timedelta


class SetSendingListView(LoginRequiredMixin, ListView):
    model = SetSending
    ordering = ['pk']


class SetSendingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = SetSending
    success_url = reverse_lazy('SetSending:list')
    permission_required = 'SetSending.delete_SetSending'


@login_required
@permission_required('SetSending.add_SetSending')
def add_sending(request):
    """
    Процедура ввода новой рассылки
    :param request:
    """
    dataset = SetSending()

    dataset.time_start = DateTimeNow.current_datetime()
    dataset.time_end = DateTimeNow.current_datetime()
    dataset.time_end = dataset.time_end + timedelta(days=1)

    client_list = Client.objects.filter(user=request.user.pk)
    list_message = Message.objects.filter(user=request.user.pk)

    if request.method == 'POST':
        set_data(request, dataset)
        dataset.user = request.user

        time_delta = (dataset.time_end - dataset.time_start).total_seconds()

        if time_delta >= float(dataset.interval):
            dataset.save()

            if dataset.status == Status.Running:
                jobs = JobService()
                jobs.add_job(request, dataset)

            messages.add_message(request, messages.SUCCESS, f'Данные #{dataset.pk} успешно сохранены!')

            return redirect(reverse('SetSending:list'))
        else:
            messages.add_message(request, messages.ERROR, 'Задание имеет неверное значение периода!')

    data = {'interval': dataset.interval,
            'status': dataset.status,
            'time_start': dataset.time_start.strftime("%Y-%m-%dT%H:%M"),
            'time_end': dataset.time_end.strftime("%Y-%m-%dT%H:%M"),
            'interval_list': INTERVALS,
            'status_list': Status.rus_list,
            'list_message': list_message,
            'client_list': client_list,
            }
    return render(request, 'SetSending/SetSending_form_new.html', data)


@login_required
@permission_required('SetSending.change_SetSending')
def edit_sending(request, pk):
    """
    Процедура обновления данных рассылки
    :param request:
    :param pk: ключ записи
    """

    dataset = SetSending.objects.get(id=pk)

    client_list = Client.objects.filter(user=request.user.pk)

    list_message = Message.objects.filter(user=request.user.pk)

    if request.method == 'POST':

        set_data(request, dataset)

        time_delta = (dataset.time_end - dataset.time_start).total_seconds()

        if time_delta >= float(dataset.interval):
            dataset.save()

            jobs = JobService()
            if dataset.status == Status.Running:
                jobs.add_job(request, dataset)

            messages.add_message(request, messages.SUCCESS, f'Данные #{dataset.pk} успешно сохранены!')
            return redirect(reverse('SetSending:list'))
        else:
            messages.add_message(request, messages.ERROR, f'Задание имеет неверное значение периода!')

    data = {'interval': int(dataset.interval),
            'time_start': dataset.time_start.strftime("%Y-%m-%dT%H:%M"),
            'time_end': dataset.time_end.strftime("%Y-%m-%dT%H:%M"),
            'status': int(dataset.status),
            'list_message': list_message,
            'interval_list': INTERVALS,
            'status_list': Status.rus_list,
            'list_address': str(dataset.list_address),
            'id_message': int(dataset.message_id),
            'client_list': client_list,
            'SetSending_id': int(dataset.pk),
            }

    return render(request, 'SetSending/SetSending_form_new.html', context=data)


def set_data(request, dataset):
    dataset.time_start = datetime.strptime(request.POST.get('time_start'), "%Y-%m-%dT%H:%M")
    dataset.time_end = datetime.strptime(request.POST.get('time_end'), "%Y-%m-%dT%H:%M")
    dataset.status = int(request.POST.get('status_list'))
    dataset.message_id = int(request.POST.get('list_message'))
    dataset.interval = int(request.POST.get('interval_list'))
    dataset.list_address = request.POST.get("list_address")

