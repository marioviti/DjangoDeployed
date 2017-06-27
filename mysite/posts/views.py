# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm

# Create your views here.

def post_create(req):
    form = PostForm(req.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(req, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(req, "Error upon create")
    context = {
        'form':form
    }
    return render(req, "form.html", context)

def post_update(req, pk=None):
    instance = get_object_or_404(Post, id=pk)
    form = PostForm(req.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(req, "Successfully updated")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(req, "Error upon update")
    context = {
        'title':instance.title,
        'instance':instance,
        'form':form
    }
    return render(req, "form.html", context)

def post_delete(req, pk=None):
    instance = get_object_or_404(Post, id=pk)
    instance.delete()
    messages.success(req, "Successfully deleted")
    return redirect('posts:list')

def post_list(req):
    page_title = 'articoli'
    queryset_list = Post.objects.all()#.order_by("-timestamp")
    paginator = Paginator(queryset_list, 5)
    page = req.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(1)
    context = {
        'page_title':page_title,
        'queryset':queryset
    }
    return render(req, "list.html", context)

def post_detail(req, pk=None):
    item = get_object_or_404(Post, pk=pk)
    context = {
        'item':item
    }
    return render(req, "detail.html", context)

def post_home(req):
    queryset = Post.objects.all()
    context = {
        'queryset':queryset
    }
    return render(req, "index.html", context)

def post_read(req):
    return HttpResponse("<h1>Read</h1>")
