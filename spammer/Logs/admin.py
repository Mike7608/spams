from django.contrib import admin

from Logs.models import Logs


@admin.register(Logs)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'job', 'status', 'description')
    list_filter = ('job', 'status',)
    search_fields = ('id', 'time',)
