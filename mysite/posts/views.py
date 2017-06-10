# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def post_home(req):
    return HttpResponse("<h1>Hi</h1>")
