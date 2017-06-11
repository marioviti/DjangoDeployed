# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def post_home(req):
    return HttpResponse("<h1>Hello</h1>")

def post_create(req):
    return HttpResponse("<h1>Create</h1>")

def post_update(req):
    return HttpResponse("<h1>Update</h1>")

def post_remove(req):
    return HttpResponse("<h1>Remove</h1>")

def post_display(req):
    return HttpResponse("<h1>Display</h1>")
