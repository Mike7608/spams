from django import forms

from SetSending.models import SetSending
from message.models import Message


class SetSendingForm(forms.ModelForm):

    class Meta:
        model = SetSending
        fields = ['time_start', 'time_end', 'interval', 'status', 'list_address', 'message']


class FormSending(forms.Form):
    #  ПРОБНАЯ РАБОТА В ВИДЖЕТАМИ
    time_start = forms.DateTimeField()
    time_end = forms.DateTimeField()
    interval = forms.IntegerField()
    status = forms.IntegerField()
    list_address = forms.CharField()
    message = forms.ModelChoiceField(queryset=Message.objects.all())

