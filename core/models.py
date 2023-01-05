from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Lead(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=30)
    message = models.TextField()
    email = models.EmailField()
    remarks = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    def __unicode__(self):
        return self.name