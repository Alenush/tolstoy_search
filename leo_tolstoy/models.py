from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Works(models.Model):
    filename = models.CharField(max_length=200)
    value = models.IntegerField()
    author = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    date = models.IntegerField()
    time = models.CharField(max_length=20)
    sphere = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    dop = models.CharField(max_length=200)
    cycle = models.CharField(max_length=200)
    finished = models.CharField(max_length=200)
    edited = models.CharField(max_length=200)
    fin_ver = models.CharField(max_length=200)
    orpho = models.CharField(max_length=200)
    source = models.CharField(max_length=200)

    def __str__(self):
        return self.name