from django.urls import path
from SetSending.apps import SetsendingConfig
from SetSending.views import SetSendingListView, SetSendingDeleteView, add_sending, edit_sending

app_name = SetsendingConfig.name

urlpatterns = [
    path('', SetSendingListView.as_view(), name='list'),
    path('create/', add_sending, name='create'),
    # path('create/', SetSendingCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', edit_sending, name='update'),
    path('delete/<int:pk>/', SetSendingDeleteView.as_view(), name='delete'),
]
