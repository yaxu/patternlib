from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import PatternForm
import json

def index(request):
    patterns = Pattern.objects.order_by('-id')[:16]
    context = {'patterns': patterns}
    return render(request, 'pattern/index.html', context)

def add(request):
    if request.method == "POST":
        form = PatternForm(request.POST)
        if form.is_valid():
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

            if pattern.typecheck():
                pattern.render()
            pattern.save()
            return redirect('pattern_detail', pk=pattern.pk)
    else:
        form = PatternForm()
    context = {'form': form}
    return render(request, 'pattern/add.html', context)

def pattern_detail(request, pk):
    pattern = get_object_or_404(Pattern, pk=pk)
    return render(request, 'pattern/detail.html', {'pattern': pattern})

def logout(request):
    auth_logout(request)
    return redirect('/')
