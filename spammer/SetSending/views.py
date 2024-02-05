from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
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

    def get_queryset(self):
        # Фильтрация данных модели
        queryset = super().get_queryset()
        filtered_data = queryset.filter(user_id=self.request.user.pk)
        return filtered_data


class SetSendingDeleteView(LoginRequiredMixin,  DeleteView):
    model = SetSending
    success_url = reverse_lazy('SetSending:list')


@login_required
def add_sending(request):
    """
    Процедура ввода новой рассылки
    :param request:
    """
    dataset = SetSending()

    dataset.time_start = datetime.now()
    dataset.time_end = dataset.time_start + timedelta(days=1)

    client_list = Client.objects.filter(user=request.user.pk)

    list_message = Message.objects.filter(user=request.user.pk)

    if request.method == 'POST':
        set_data(request, dataset)
        dataset.user = request.user

        time_delta = (dataset.time_end - dataset.time_start).total_seconds()

        if time_delta >= float(dataset.interval):
            dataset.save()

            save_select_client(request, dataset)  # сохраняем выбранных клиентов

            if dataset.status == Status.Running:
                jobs = JobService()
                jobs.add_job(request, dataset)

            messages.add_message(request, messages.SUCCESS, f'Данные #{dataset.pk} успешно сохранены!')

            return redirect(reverse('SetSending:list'))
        else:
            messages.add_message(request, messages.ERROR, 'Задание имеет неверное значение периода!')

    data = {'interval': dataset.interval,
            'status': dataset.status,
            'time_start': dataset.time_start,
            'time_end': dataset.time_end,
            'interval_list': INTERVALS,
            'status_list': Status.rus_list,
            'list_message': list_message,
            'client_list': client_list,
            }
    return render(request, 'SetSending/SetSending_form_new.html', data)


@login_required
def edit_sending(request, pk):
    """
    Процедура обновления данных рассылки
    :param request:
    :param pk: ключ записи
    """

    dataset = SetSending.objects.get(id=pk)

    client_list_temp = Client.objects.filter(user=request.user.pk)
    client_list_use = dataset.client.all()

    client_list = list(set(client_list_temp) - set(client_list_use))

    list_message = Message.objects.filter(user=request.user.pk)

    if request.method == 'POST':

        set_data(request, dataset)

        time_delta = (dataset.time_end - dataset.time_start).total_seconds()

        if time_delta >= float(dataset.interval):
            dataset.save()

            save_select_client(request, dataset)  # сохраняем выбранных клиентов

            jobs = JobService()
            if dataset.status == Status.Running:
                jobs.add_job(request, dataset)

            messages.add_message(request, messages.SUCCESS, f'Данные #{dataset.pk} успешно сохранены!')
            return redirect(reverse('SetSending:list'))
        else:
            messages.add_message(request, messages.ERROR, f'Задание имеет неверное значение периода!')

    data = {'interval': int(dataset.interval),
            'time_start': dataset.time_start,
            'time_end': dataset.time_end,
            'status': int(dataset.status),
            'list_message': list_message,
            'interval_list': INTERVALS,
            'status_list': Status.rus_list,
            'id_message': int(dataset.message_id),
            'client_list': client_list,
            'clients': dataset.client
            }

    return render(request, 'SetSending/SetSending_form_new.html', context=data)


def set_data(request, dataset):
    dataset.time_start = datetime.strptime(request.POST.get('time_start'), "%Y-%m-%dT%H:%M")
    dataset.time_end = datetime.strptime(request.POST.get('time_end'), "%Y-%m-%dT%H:%M")
    dataset.status = int(request.POST.get('status_list'))
    dataset.message_id = int(request.POST.get('list_message'))
    dataset.interval = int(request.POST.get('interval_list'))
    dataset.list_address = request.POST.get("list_address")


def save_select_client(request, dataset):
    """
    Процедура сохраняет выбранных клиентов
    :param request:
    :param dataset:
    :return:
    """
    selected_clients = request.POST.getlist('client_list_select')
    dataset.client.clear()
    for item in selected_clients:
        cl = Client.objects.get(id=item)
        dataset.client.add(cl)
        dataset.save()
