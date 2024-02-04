from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from message.forms import MessageForm
from message.models import Message


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    ordering = ['pk']

    def get_queryset(self):
        # Фильтрация данных модели
        queryset = super().get_queryset()
        filtered_data = queryset.filter(user_id=self.request.user.pk)
        return filtered_data


class MessageCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:list')
    success_message = 'Новое письмо для рассылки успешно сохранено!'

    def form_valid(self, form):
        new_message = form.save(commit=False)
        new_message.user = self.request.user
        new_message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:list')
    success_message = 'Изменения сообщения успешно сохранены!'

    def form_valid(self, form):
        new_message = form.save(commit=False)
        new_message.save()
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin,  SuccessMessageMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('message:list')
    success_message = 'Сообщение успешно удалено!'

