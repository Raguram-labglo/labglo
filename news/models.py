from __future__ import unicode_literals
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse


class Tag(models.Model):
    """ Model to save all tags, related to news """
    name = models.CharField(max_length=252, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class News(models.Model):
    """ Model to save all news """
    title = models.CharField(max_length=512)
    slug = models.SlugField(max_length=128, unique=True)
    is_active = models.BooleanField(default=True)           # To check news expired or not
    description = RichTextUploadingField()
    image_url = models.URLField(max_length=512, blank=True, null=True)
    source = models.URLField(max_length=512, blank=True, null=True)
    tag = models.ManyToManyField(Tag, related_name='tags')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:news_details", kwargs={'slug':self.slug})