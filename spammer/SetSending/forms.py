from django import forms
from SetSending.models import SetSending
from message.models import Message
from spammer.services import StyleFormMixin


class SetSendingForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = SetSending
        fields = ['time_start', 'time_end', 'interval', 'status', 'list_address', 'message']


class AddSending(forms.Form):
    time_start = forms.DateTimeField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'}), label='Время начала рассылки')
    time_end = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    interval = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.ModelChoiceField(queryset=Message.objects.all())
