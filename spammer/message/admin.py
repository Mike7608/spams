from django.contrib import admin

from message.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'message', 'user')
    list_filter = ('user',)
    search_fields = ('subject', )
