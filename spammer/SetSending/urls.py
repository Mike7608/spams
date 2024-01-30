from django.urls import path
from SetSending.apps import SetsendingConfig
from SetSending.views import SetSendingListView, SetSendingUpdateView, SetSendingDeleteView, SetSendingCreateView

app_name = SetsendingConfig.name

urlpatterns = [
    path('', SetSendingListView.as_view(), name='list'),
    path('create/', SetSendingCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', SetSendingUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', SetSendingDeleteView.as_view(), name='delete'),
]
