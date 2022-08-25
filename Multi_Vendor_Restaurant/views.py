from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Hello we are starting the project Its Lite Im PUMPED...</h1>")