from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import PatternForm

def index(request):
    context = {}
    return render(request, 'pattern/index.html', context)

def add(request):
    context = {'form': PatternForm()}
    return render(request, 'pattern/add.html', context)

def logout(request):
    auth_logout(request)
    return redirect('/')
