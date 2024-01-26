from django.urls import path
from message.apps import MessageConfig
from message.views import MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = MessageConfig.name

urlpatterns = [
    path('', MessageListView.as_view(), name='list'),
    path('create/', MessageCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', MessageUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', MessageDeleteView.as_view(), name='delete'),
]