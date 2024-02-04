from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from message.forms import MessageForm
from message.models import Message


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    ordering = ['pk']


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:list')
    permission_required = 'Message.add_Message'
    success_message = 'Новое письмо для рассылки успешно сохранено!'

    def form_valid(self, form):
        new_message = form.save(commit=False)
        new_message.user = self.request.user
        new_message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:list')
    permission_required = 'Message.change_Message'
    success_message = 'Изменения сообщения успешно сохранены!'

    def form_valid(self, form):
        new_message = form.save(commit=False)
        new_message.save()
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('message:list')
    permission_required = 'Message.delete_Message'
    success_message = 'Сообщение успешно удалено!'
