from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from SetSending.forms import SetSendingForm, FormSending
from SetSending.models import SetSending
from spammer.services import JobService


class SetSendingListView(ListView):
    model = SetSending
    ordering = ['pk']


class SetSendingCreateView(CreateView):
    model = SetSending
    form_class = SetSendingForm
    success_url = reverse_lazy('SetSending:list')

    def form_valid(self, form):
        new_setting = form.save(commit=False)
        new_setting.user = self.request.user
        new_setting.save()
        jobs = JobService()
        jobs.add_job(new_setting.time_start, new_setting.time_end, new_setting.interval, new_setting.pk)
        return super().form_valid(form)


class SetSendingUpdateView(UpdateView):
    model = SetSending
    form_class = SetSendingForm
    success_url = reverse_lazy('SetSending:list')

    def form_valid(self, form):
        new_message = form.save(commit=False)
        new_message.save()
        return super().form_valid(form)


class SetSendingDeleteView(DeleteView):
    model = SetSending
    success_url = reverse_lazy('SetSending:list')


def add_sending(request):
    form = FormSending
    data = {
            'form': form,
            }
    return render(request, 'SetSending/SetSending_form_new.html', data)


def edit_sending(request, pk):

    dat = SetSending.objects.get(id=pk)  # Получаем объект модели для редактирования

    form = FormSending  # Отображаем форму с заполненными данными объекта модели
    form.data = dat

    data = {'interval': dat.interval, 'time_start': dat.time_start.strftime("%Y-%m-%dT%H:%M:%S"),
            'time_end': dat.time_end.strftime("%Y-%m-%dT%H:%M:%S"), 'status': dat.status,
            'list_address': dat.list_address, 'message': dat.message}

    return render(request, 'SetSending/SetSending_form_new.html', data)


def save_sending(request, pk):

    instance = SetSending.objects.get(id=pk)  # Получаем объект модели для редактирования

    if request.method == 'POST':
        form = FormSending(request.POST, instance) # Привязываем данные к форме
        if form.is_valid():
            form.save()  # Сохраняем изменения
            # Добавьте здесь код для редиректа или отображения страницы с подтверждением
    else:
        form = FormSending(instance)  # Отображаем форму с заполненными данными объекта модели

    data = {
            'form': form,
            }
    return render(request, 'SetSending/SetSending_form_new.html', data)