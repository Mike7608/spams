from django import forms

from SetSending.models import SetSending


class SetSendingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = SetSending
        fields = ['time_start', 'time_end', 'interval', 'status', 'client', 'message']

