from django.contrib import admin

from clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name')
    list_filter = ('name', 'email')
    search_fields = ('name', 'description')

