#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json

data_file = open(u'index.json')
index_data = json.load(data_file)

# Create your models here.
class OriginalWorks(models.Model):
    filename = models.CharField(max_length=200,null=True)
    value = models.IntegerField(null=True)
    author = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200)
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

class TeiWorks(models.Model):
    filename = models.CharField(max_length=200,null=True)
    value = models.IntegerField(null=True)
    author = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200)
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


class MyUser(models.Model):
    message = models.CharField(max_length=1000)
    email = models.EmailField()

class LemmasInverseTable(models.Model):
    lemma = models.CharField(db_index=True,max_length=200)
    documents = models.TextField(db_index=True) # [ [название_файла,страница,айдипараграфа], ... ]

class TolstoyTexts(models.Model):
    filename = models.CharField(db_index=True,max_length=500) # название файла
    page = models.IntegerField()
    par_index = models.IntegerField(db_index=True) #индекс параграфа
    paragraphs = models.TextField(db_index=True) # сам параграф
    html_link = models.CharField(db_index=True,max_length=500) # html part
