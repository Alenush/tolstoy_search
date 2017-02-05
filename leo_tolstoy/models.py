#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.db import models

# Create your models here.
class OriginalWorks(models.Model):
    filename = models.CharField(db_index=True,max_length=200,null=True)
    value = models.IntegerField(db_index=True,null=True)
    author = models.CharField(db_index=True,max_length=200,null=True)
    name = models.CharField(db_index=True,max_length=200)
    date = models.IntegerField(db_index=True,null=True)
    place = models.CharField(db_index=True,max_length=50, null=True)
    time = models.CharField(db_index=True,max_length=20, null=True)
    sphere = models.CharField(db_index=True,max_length=200)
    type = models.CharField(db_index=True,max_length=200, null=True)
    topic = models.CharField(db_index=True,max_length=200, null=True)
    dop = models.CharField(db_index=True,max_length=200, null=True)
    cycle = models.CharField(db_index=True,max_length=200, null=True)
    finished = models.CharField(db_index=True,max_length=200, null=True)
    edited = models.CharField(db_index=True,max_length=200, null=True)
    fin_ver = models.CharField(db_index=True,max_length=200, null=True)
    orpho = models.CharField(db_index=True,max_length=200, null=True)
    source = models.CharField(db_index=True,max_length=200, null=True)

    def __str__(self):
        try:
            return self.name
        except:
            return "%s" % self.pk

class MyUser(models.Model):
    message = models.CharField(max_length=1000)
    email = models.EmailField()

class LemmasInverseTable(models.Model):
    lemma = models.CharField(db_index=True,max_length=200, null=True)
    documents = models.TextField(db_index=True,null=True)
    type = models.TextField(db_index=True,null=True)

class TolstoyTexts(models.Model):
    filename = models.CharField(db_index=True,max_length=500)
    page = models.IntegerField(db_index=True)
    par_index = models.IntegerField(db_index=True)
    paragraphs = models.TextField(db_index=True)
    html_link = models.CharField(db_index=True,max_length=200)

class TolstoyLetters(models.Model):
    filename = models.CharField(db_index=True,max_length=500)
    page = models.IntegerField(db_index=True)
    par_index = models.IntegerField(db_index=True)
    paragraphs = models.TextField(db_index=True)
    html_link = models.CharField(db_index=True,max_length=200)

class Letters(models.Model):
    filename = models.CharField(db_index=True, max_length=1000)
    id_name = models.CharField(db_index=True, max_length=1000)
    value = models.IntegerField(db_index=True,null=True)
    name = models.CharField(db_index=True, max_length=1000)
    number = models.IntegerField(db_index=True, null=True)
    addressee = models.CharField(db_index=True, max_length=1000)
    date1 = models.CharField(db_index=True, max_length=1000)
    date2 = models.CharField(db_index=True, max_length=1000)
    place = models.CharField(db_index=True, max_length=1000)
    type = models.CharField(db_index=True, max_length=1000)
    source = models.CharField(db_index=True, max_length=1000)

