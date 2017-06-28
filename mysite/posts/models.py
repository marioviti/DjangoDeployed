# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
import os

# Create your models here.

def upload_location(instance, filename):
    return os.path.join('posts', instance.slug, filename)

class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True,
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

def create_slug(instance, new_slug=None):
    slug=slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().pk)
        return create_slug(instance, new_slug)
    return slug

def pre_save_post_reveiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_reveiver, sender=Post)
