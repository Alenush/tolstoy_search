#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import os
import zipfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import codecs

from leo_tolstoy.models import Works


def index(request):
    return render(request, 'index.html')

def show_data(request):
    all_works = Works.objects.all()
    paginator = Paginator(all_works, 100)
    page = request.GET.get('page')
    try:
         my_works = paginator.page(page)
    except PageNotAnInteger:
        my_works = paginator.page(1)
    except EmptyPage:
        my_works = paginator.page(paginator.num_pages)
    return render(request, 'data.html', {"works":my_works, 'volums':[]})

def show_chudozh(request):
    chudozh = set()
    for works in Works.objects.filter(sphere='художественная'):
        chudozh.add(works)
    paginator = Paginator(list(chudozh), 60)
    page = request.GET.get('page')
    try:
        chud_works = paginator.page(page)
    except PageNotAnInteger:
        chud_works = paginator.page(1)
    except EmptyPage:
        chud_works = paginator.page(paginator.num_pages)

    return render(request, 'data.html', {"works": chud_works})

def show_volums(request):
    volums = set()
    for works in Works.objects.all():
        volums.add(works.value)
    return render(request, 'data.html', {"works": [], 'volums': volums})

def show_public(request):
    public = set()
    for works in Works.objects.filter(sphere='публицистика'):
        public.add(works)
    paginator = Paginator(list(public), 60)
    page = request.GET.get('page')
    try:
        public_works = paginator.page(page)
    except PageNotAnInteger:
        public_works = paginator.page(1)
    except EmptyPage:
        public_works = paginator.page(paginator.num_pages)
    return render(request, 'data.html', {"works": public_works})

def show_diaries(request):
    diaries = set()
    for works in Works.objects.filter(sphere='дневники и записные книжки'):
        diaries.add(works)
    return render(request, 'data.html', {"works": diaries})

def show_letters(request):
    letters = set()
    for works in Works.objects.filter(sphere='Личная и деловая переписка'):
        letters.add(works)
    paginator = Paginator(list(letters), 100)
    page = request.GET.get('page')
    try:
        letters_works = paginator.page(page)
    except PageNotAnInteger:
        letters_works = paginator.page(1)
    except EmptyPage:
        letters_works = paginator.page(paginator.num_pages)
    return render(request, 'data.html', {"works": letters_works})

def show_children(request):
    children = set()
    for works in Works.objects.filter(sphere='детская литература'):
        children.add(works)
    return render(request, 'data.html', {"works": children})

def show_church(request):
    church = set()
    for works in Works.objects.filter(sphere='Церковно-богословская литература'):
        church.add(works)
    return render(request, 'data.html', {"works": church})

def find_doc(request):
    search_works = set()
    if request.method == "POST":
        query = request.POST.get('query')
        print('REQUEST', query)
        for works in Works.objects.filter(name__contains=query):
            search_works.add(works)
    return render(request, 'data.html', {"works": search_works})

def start_search(request):
    vol_array = range(1,91)
    years = set()
    for works in Works.objects.all():
        if works.date != None and works.date != '?' and works.date!='0':
            years.add(works.date)
    return render(request, 'search.html', {'vol_array':vol_array, 'years': sorted(years)})

def all_files_download(request, tag):
    """
    Download xml files
    :param tag: all, vol_n, file
    :return:
    """
    # print("Tag from template: ", tag)
    dic_of_docs = {'all':'xml_data.zip'}
    for folder in os.listdir(os.path.realpath(os.getcwd())+'/leo_tolstoy/xml_data/'):
        if folder.endswith('zip'):
            vol = folder.split('.')[0].replace('_','')
            dic_of_docs[vol] = folder
    global path_to_file
    if 'xhtml' in tag:
        for root, dirs, filenames in os.walk(os.getcwd()+'/leo_tolstoy/xml_data/'):
            for filename in filenames:
                if os.path.split(filename)[-1].decode('utf-8') == tag:
                    path_to_file = os.path.join(root, filename)
    else:
         if 'vol' in tag:
             tag = tag.split('vol')[1]
             path_to_file = os.path.dirname(os.path.realpath(__file__)) + "/xml_data/"+dic_of_docs.get(str(tag))
    my_file = open(path_to_file, 'r')
    response = HttpResponse(my_file, content_type='application/force-download')
    if tag == 'all':
        response['Content-Disposition'] = 'attachment; filename=%s' % 'all_xml.zip'
    else:
        response['Content-Disposition'] = 'attachment; filename=%s' % path_to_file.split('/')[-1]
    return response


def search_big(request):
    """

    :param request:
    """
    if request.method == "POST":

        if request.POST.get('search_big_input'):
            print('BIG search')
            results = []
            return render(request, 'text_search_out.html', {'res_docs': results})
        else:
            print('Meta search!')
            docs = []
            return render(request, 'meta_search_out.html', {'res_docs': docs})

def simple_search(request):
    data = [[]]
    return render(request, 'text_search_out.html', {'res_data': data})