from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Works(models.Model):
    filename = models.CharField(max_length=200)
    value = models.IntegerField(null=True)
    author = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200,)
    date = models.IntegerField(null=True)
    place = models.CharField(max_length=50, null=True)
    time = models.CharField(max_length=20, null=True)
    sphere = models.CharField(max_length=200)
    type = models.CharField(max_length=200, null=True)
    topic = models.CharField(max_length=200, null=True)
    dop = models.CharField(max_length=200, null=True)
    cycle = models.CharField(max_length=200, null=True)
    finished = models.CharField(max_length=200, null=True)
    edited = models.CharField(max_length=200, null=True)
    fin_ver = models.CharField(max_length=200, null=True)
    orpho = models.CharField(max_length=200, null=True)
    source = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name