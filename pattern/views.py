from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import PatternForm
import json

def pattern_index(request):
    patterns = Pattern.objects.filter(status__in=['live','rendering']).order_by('-id')[:16]
    context = {'patterns': patterns}
    return render(request, 'pattern/index.html', context)

@login_required
def pattern_love(request, pk):
    if request.method == "POST":
        i = Identity.objects.get(user=request.user)
        pattern = get_object_or_404(Pattern, pk=pk)
        pattern.lovePattern(i)
    return redirect('pattern_detail', pk=pattern.pk)        

@login_required
def pattern_unlove(request, pk):
    if request.method == "POST":
        i = Identity.objects.get(user=request.user)
        pattern = get_object_or_404(Pattern, pk=pk)
        print("unlove")
        pattern.unlovePattern(i)
    return redirect('pattern_detail', pk=pattern.pk)        

@login_required
def pattern_add(request, parent_pk=None): 
    if parent_pk:
        parent = get_object_or_404(Pattern, pk=parent_pk, status='live')
    else:
        parent = None
 
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
            pattern.parent = parent
            pattern.save()
            
            if pattern.typecheck():
                pattern.render()
                pattern.save()
                
            return redirect('pattern_detail', pk=pattern.pk)
    else:
        form = PatternForm()
    context = {'form': form, 'parent': parent}
    return render(request, 'pattern/add.html', context)

def pattern_detail(request, pk):
    pattern = get_object_or_404(Pattern, pk=pk)
    pattern.is_live() # fixes status if necessary
    loves = False
    if request.user.is_authenticated:
        i = Identity.objects.get(user=request.user)
        if i.pattern_loves.filter(id=pattern.id).exists():
            loves = True
    
    return render(request, 'pattern/detail.html', {'pattern': pattern, 'loves': loves})

def pattern_person(request, ident):
    i = get_object_or_404(Identity, ident=ident)
    patterns = Pattern.objects.filter(status='live', author=i)
    return render(request, 'pattern/person.html', {'identity': i, 'patterns': patterns})

def logout(request):
    auth_logout(request)
    return redirect('/')
