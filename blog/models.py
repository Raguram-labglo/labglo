from __future__ import unicode_literals
from datetime import date
from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Tag(models.Model):
    """ Model to save all tags, related to blog """
    name = models.CharField(max_length=252, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    """ Model to save all post related to blog app
    - Tag: multiple selection available
    - Publish date: default today(editable)
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=512)
    slug = models.SlugField(max_length=512, unique=True, db_index=True)
    summary = models.TextField(null=True, blank=True)
    content = RichTextField()
    is_published = models.BooleanField(default=True)
    publish_date = models.DateField(default=date.today, editable=True)
    tags = models.ManyToManyField(Tag)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        date = self.created_on
        return reverse("blog:post_details", kwargs={'slug':self.slug,
            'year': date.year, 'month': date.month, 'day': date.day})