from django import forms
from message.models import Message
from spammer.services import StyleFormMixin


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = ['subject', 'message']

