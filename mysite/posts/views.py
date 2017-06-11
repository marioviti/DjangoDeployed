# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def post_home(req):
    return render(req,"index.html",{})

def post_create(req):
    return HttpResponse("<h1>Create</h1>")

def post_read(req):
    return HttpResponse("<h1>Read</h1>")

def post_update(req):
    return HttpResponse("<h1>Update</h1>")

def post_delete(req):
    return HttpResponse("<h1>Delete</h1>")

def post_list(req):
    return HttpResponse("<h1>List</h1>")
