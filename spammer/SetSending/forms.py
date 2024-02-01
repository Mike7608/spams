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
    interval = forms.IntegerField(min_value=1)
    status = forms.IntegerField(min_value=0)
    list_address = forms.CharField(widget=forms.Textarea)
    message = forms.ModelChoiceField(queryset=Message.objects.all())



