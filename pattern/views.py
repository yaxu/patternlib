from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import PatternForm
import json

def pattern_index(request):
    rendering = Pattern.objects.filter(status__in=['rendering'])
    latest = Pattern.objects.filter(status__in=['live']).order_by('-id')[:32]
    context = {'latest': latest}
    return render(request, 'pattern/index.html', context)

def pattern_about(request):
    latest = Pattern.objects.filter(status__in=['live']).order_by('-id')[:16]
    context = {'latest': latest}
    return render(request, 'pattern/about.html', context)

def pattern_help(request):
    latest = Pattern.objects.filter(status__in=['live']).order_by('-id')[:16]
    context = {'latest': latest}
    return render(request, 'pattern/help.html', context)

@login_required
def pattern_love(request, pk):
    if request.method == "POST":
        i , created = Identity.objects.get_or_create(
            user = request.user,
            service = None,
            defaults={'name': '',
                      'ident': request.user.username
                     },
            )
        pattern = get_object_or_404(Pattern, pk=pk)
        pattern.lovePattern(i)
    return redirect('pattern_detail', pk=pattern.pk)        

@login_required
def pattern_unlove(request, pk):
    if request.method == "POST":
        i , created = Identity.objects.get_or_create(
            user = request.user,
            service = None,
            defaults={'name': '',
                      'ident': request.user.username
                     },
            )
        pattern = get_object_or_404(Pattern, pk=pk)
        print("unlove")
        pattern.unlovePattern(i)
    return redirect('pattern_detail', pk=pattern.pk)        

@login_required
def pattern_edit(request, parent_pk=None, pk=None): 
    if parent_pk:
        parent = get_object_or_404(Pattern, pk=parent_pk, status='live')
    else:
        parent = None
 
    if request.method == "POST":
        if pk:
            pattern = get_object_or_404(Pattern, pk=pk)
            if pattern.author.user != request.user:
                return HttpResponseForbidden()
            pattern.editNumber = pattern.editNumber + 1
        else:
            username = request.user.username
            ident, created = Identity.objects.get_or_create(
                user = request.user,
                service = None,
                defaults={'name': '',
                          'ident': username
                },
            )
            language = Language.objects.get_or_create(
                name = "TidalCycles"
            )
            pattern = Pattern(author = ident,
                              parent = parent,
                              language = language[0]
            )
        
        form = PatternForm(request.POST or None, instance=pattern)
        if form.is_valid():
            form.save(commit=False)
            
            if pattern.getJSON():
                # needs to save (and get an id) before rendering
                pattern.save()
                pattern.render()
                pattern.save()
                return redirect('pattern_detail', pk=pattern.pk)
    else:
        if pk:
            pattern = get_object_or_404(Pattern, pk=pk)
            form = PatternForm(instance=pattern)
            code = pattern.code
            mode = "edit"
        else:
            form = PatternForm()
            mode = "add"
            if parent:
                code = parent.code
            else:
                code = ""

    context = {'form': form, 'parent': parent, 'code': code, 'mode': mode}
    return render(request, 'pattern/add.html', context)

def pattern_detail(request, pk):
    pattern = get_object_or_404(Pattern, pk=pk)
    pattern.is_live() # fixes status if necessary
    loves = False
    latest = Pattern.objects.filter(status__in=['live']).order_by('-id')[:16]
    context = {'latest': latest,
               'pattern': pattern,
               'loves': loves
              }

    if request.user.is_authenticated:
        i, created = Identity.objects.get_or_create(
              user = request.user,
              service = None,
              defaults={'name': '',
                        'ident': request.user.username
              },
            )
        if i.pattern_loves.filter(id=pattern.id).exists():
            loves = True
    
    return render(request, 'pattern/detail.html', context)

def pattern_person(request, ident):
    i = get_object_or_404(Identity, ident=ident)
    patterns = Pattern.objects.filter(status='live', author=i)
    return render(request, 'pattern/person.html', {'identity': i, 'patterns': patterns})

def logout(request):
    auth_logout(request)
    return redirect('/')
