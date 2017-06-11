"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

import views
# Guide to django regex
# https://github.com/codingforentrepreneurs/Guides/blob/master/all/common_url_regex.md

urlpatterns = [
    url(r'^$', views.post_home),
    #CRUD STUFF
    url(r'^create/$', views.post_create),
    url(r'^remove/$', views.post_remove),
    url(r'^update/$', views.post_update),
    url(r'^display/$', views.post_display),
]
