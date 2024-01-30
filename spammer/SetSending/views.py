from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from SetSending.forms import SetSendingForm, AddSending
from SetSending.models import SetSending


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
    form = AddSending
    data = {
            'form': form,
            }
    return render(request, 'SetSending/SetSending_form.html', data)
