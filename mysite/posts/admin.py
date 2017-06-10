# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Post

# Register your models here.

# Check for options for ModelAdmin
# https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#modeladmin-options

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title','updated','timestamp']
    list_display_links = ['title']
    list_filter = ['updated','timestamp']
    search_fields = ['title','content']
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
