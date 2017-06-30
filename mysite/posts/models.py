# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
import os

# Create your models here.

# """ Non si può fare
# https://docs.djangoproject.com/en/1.11/topics/migrations/#serializing-values
# def upload_location(father_dir):
#     def upload_to_location(instance,filename):
#         return os.path.join(father_dir, instance.slug, filename)
#     return upload_to_location
# """

def post_upload_to_location(instance,filename):
    return os.path.join('posts', instance.slug, filename)

def article_upload_to_location(instance,filename):
    return os.path.join('articles', instance.slug, filename)

class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=article_upload_to_location, null=True, blank=True,
        width_field="width_field",
        height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    notebook = models.FileField(upload_to=article_upload_to_location, null=True, blank=True)
    abstract = models.TextField()
    # tags = some fields... TODO
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    """python 2.7"""
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:article', kwargs={'slug':self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=post_upload_to_location, null=True, blank=True,
        width_field="width_field",
        height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    """python 2.7"""
    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post', kwargs={'slug':self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

# slug and pre_save signal stuff
# https://docs.djangoproject.com/en/1.9/ref/signals/#django.db.models.signals.pre_save

def create_slug(instance, sender, new_slug=None):
    slug=slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = sender.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().pk)
        return create_slug(instance, sender, new_slug)
    return slug

def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance,sender)

pre_save.connect(pre_save_receiver, sender=Post)
pre_save.connect(pre_save_receiver, sender=Article)
