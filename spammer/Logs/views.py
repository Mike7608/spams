from django.views.generic import ListView

from Logs.models import Logs


class LogsListView(ListView):
    model = Logs
    ordering = ['pk']
