from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
#from .models import Event, Artist, Festival

def index(request):
    context = {}
    return render(request, 'pattern/index.html', context)
