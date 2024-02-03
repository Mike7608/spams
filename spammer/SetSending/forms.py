from django import forms

from SetSending.models import SetSending
from message.models import Message


class SetSendingForm(forms.ModelForm):

    class Meta:
        model = SetSending
        fields = ['time_start', 'time_end', 'interval', 'status', 'list_address', 'message']




