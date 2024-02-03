from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DeleteView
from SetSending.models import SetSending
from clients.models import Client
from message.models import Message
from spammer.services import JobService, Status
from spammer.settings import INTERVALS
from datetime import datetime


class SetSendingListView(ListView):
    model = SetSending
    ordering = ['pk']


# class SetSendingCreateView(CreateView):
#     model = SetSending
#     form_class = SetSendingForm
#     success_url = reverse_lazy('SetSending:list')
#
#     def form_valid(self, form):
#         new_setting = form.save(commit=False)
#         new_setting.user = self.request.user
#         new_setting.save()
#         jobs = JobService()
#         jobs.add_job(new_setting.time_start, new_setting.time_end, new_setting.interval, new_setting.pk)
#         return super().form_valid(form)


# class SetSendingUpdateView(UpdateView):
#     model = SetSending
#     form_class = SetSendingForm
#     success_url = reverse_lazy('SetSending:list')
#
#     def form_valid(self, form):
#         new_message = form.save(commit=False)
#         new_message.save()
#         return super().form_valid(form)


class SetSendingDeleteView(DeleteView):
    model = SetSending
    success_url = reverse_lazy('SetSending:list')


def add_sending(request):
    """
    Процедура ввода новой рассылки
    :param request:
    """
    dataset = SetSending()
    dataset.time_start = datetime.now()
    dataset.time_end = datetime.now()

    client_list = Client.objects.filter(user=request.user.pk)
    list_message = Message.objects.filter(user=request.user.pk)

    if request.method == 'POST':
        set_data(request, dataset)
        dataset.user = request.user

        time_delta = (dataset.time_end - dataset.time_start).total_seconds()

        if time_delta >= float(dataset.interval):
            dataset.save()

            jobs = JobService()
            jobs.add_job(dataset.time_start, dataset.time_end, dataset.interval, dataset.pk)

            messages.add_message(request, messages.SUCCESS, 'Данные успешно сохранены!')

            return redirect(reverse('SetSending:list'))
        else:
            messages.add_message(request, messages.ERROR, 'Ошибочное значение периода!')

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
            messages.add_message(request, messages.SUCCESS, 'Данные успешно сохранены!')
            return redirect(reverse('SetSending:list'))
        else:
            messages.add_message(request, messages.ERROR, 'Ошибочное значение периода!')

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

