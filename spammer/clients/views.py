from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from clients.forms import ClientForm
from clients.models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    ordering = ['pk']


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:list')
    permission_required = 'client.add_client'
    success_message = "Данные нового клиента успешно сохранены!"

    def form_valid(self, form):
        new_client = form.save(commit=False)
        new_client.user = self.request.user
        new_client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:list')
    permission_required = 'client.change_client'
    success_message = "Данные клиента успешно обновлены!"

    def form_valid(self, form):
        new_client = form.save(commit=False)
        new_client.save()
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients:list')
    permission_required = 'client.delete_client'
    success_message = "Клиент был успешно удален!"

