from django.urls import path

from .apps import LogsConfig
from .views import LogsListView

app_name = LogsConfig.name

urlpatterns = [
    path('', LogsListView.as_view(), name='list'),
]
