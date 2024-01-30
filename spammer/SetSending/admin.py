from django.contrib import admin

from SetSending.models import SetSending


@admin.register(SetSending)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'time_start', 'time_end', 'interval', 'message', 'status', 'user')
    list_filter = ('time_start', 'time_end', 'status', 'user')
    search_fields = ('id', 'time_start', 'time_end', )
