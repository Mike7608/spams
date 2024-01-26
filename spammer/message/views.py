from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from message.forms import MessageForm
from message.models import Message


class MessageListView(ListView):
    model = Message
    ordering = ['pk']


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:list')

    def form_valid(self, form):
        new_message = form.save(commit=False)
        new_message.user = self.request.user
        new_message.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:list')

    def form_valid(self, form):
        new_message = form.save(commit=False)
        new_message.save()
        return super().form_valid(form)


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('message:list')
