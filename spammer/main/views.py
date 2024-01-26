from django.shortcuts import render
from .apps import MainConfig

app_name = MainConfig.name


def index(request):

    r = render(request, 'home.html')
    return r
