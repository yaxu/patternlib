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
    if request.method == "POST":
        form = PatternForm(request.POST)
        pattern = form.save(commit=False)
        username = request.user.username
        language = Language.objects.get_or_create(
            name = "TidalCycles"
        );
        pattern.language = language[0]
        ident = Identity.objects.get_or_create(
            user = request.user,
            service = None,
            defaults={'name': '',
                      'ident': username
            },
        ),
        pattern.author = ident[0][0]
        pattern.save()
    else:
        form = PatternForm()
    context = {'form': form}
    return render(request, 'pattern/add.html', context)

def logout(request):
    auth_logout(request)
    return redirect('/')
