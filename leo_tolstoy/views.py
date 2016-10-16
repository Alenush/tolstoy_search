#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import os
import zipfile

from leo_tolstoy.models import Works


def index(request):
    return render(request, 'index.html')

def show_data(request):
    print("Length: ", len(Works.objects.all()))
    all_works = Works.objects.all()[1000:1200]
    volums = set()
    for works in Works.objects.all():
        volums.add(works.value)
    return render(request, 'data.html', {"works":all_works, 'volums':volums})

def start_search(request):
    vol_array = range(1,91)
    return render(request, 'search.html', {'vol_array':vol_array})

def all_files_download(request, tag):
    """
    Download xml files
    :param tag: all, vol_n, file
    :return:
    """
    print("Tag from template: ", tag)
    dic_of_docs = {'all':'xml_data.zip'}
    for folder in os.listdir(os.path.realpath(os.getcwd())+'/leo_tolstoy/xml_data/'):
        if folder.endswith('zip'):
            vol = folder.split('.')[0].replace('_','')
            dic_of_docs[vol] = folder
    if 'xhtml' in tag:
        for filename, dirs, data_array in os.walk(os.getcwd()+'/leo_tolstoy/xml_data/'):
            tag = str(tag).encode('utf8')
            if tag in data_array:
                new_tag = filename+'/'+tag
                path_to_file = str(new_tag)
                dic_of_docs[tag] = tag
    else:
        if 'vol' in tag:
            tag = tag.split('vol')[1]
            print("VOL ", tag)
        path_to_file = os.path.dirname(os.path.realpath(__file__)) + "/xml_data/"+dic_of_docs.get(str(tag))
    my_file = open(path_to_file, 'r')
    response = HttpResponse(my_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % dic_of_docs[str(tag)]
    return response