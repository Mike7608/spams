from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from clients.forms import ClientForm
from clients.models import Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    ordering = ['pk']

    def get_queryset(self):
        # Фильтрация данных модели
        queryset = super().get_queryset()
        filtered_data = queryset.filter(user_id=self.request.user.pk)
        return filtered_data


class ClientCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:list')
    success_message = "Данные нового клиента успешно сохранены!"

    def form_valid(self, form):
        new_client = form.save(commit=False)
        new_client.user = self.request.user
        new_client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('clients:list')
    success_message = "Данные клиента успешно обновлены!"

    def form_valid(self, form):
        new_client = form.save(commit=False)
        new_client.save()
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients:list')
    success_message = "Клиент был успешно удален!"

