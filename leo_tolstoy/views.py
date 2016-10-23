#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import os
from BeautifulSoup import BeautifulStoneSoup

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import codecs
import sys
streamWriter = codecs.lookup('utf-8')[-1]
sys.stdout = streamWriter(sys.stdout)

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
            if type(works.date)!='unicode':
                years.add(works.date)
    return render(request, 'search.html', {'vol_array':vol_array, 'years': sorted(years)})

def all_files_download(request, tag):
    """
    Download xml files
    :param tag: all, vol_n, file
    :return:
    """
    dic_of_docs = {'all':'xml_data.zip'}
    for folder in os.listdir(os.path.realpath(os.getcwd())+'/leo_tolstoy/xml_data/'):
        if folder.endswith('zip'):
            vol = folder.split('.')[0].replace('_','')
            dic_of_docs[vol] = folder
    global path_to_file
    for root, dirs, filenames in os.walk(os.getcwd()+'/leo_tolstoy/xml_data/'):
        if 'xhtml' in tag:
            for filename in filenames:
                if os.path.split(filename)[-1].decode('utf-8') == tag:
                    new_path = os.path.join(root, filename)
                    new_tag = new_path.split('/')[-2:]
                    dic_of_docs[tag] = '/'.join(new_tag)
                else:
                    print('WTF', tag, os.path.split(filename)[-1].decode('utf-8'))
        elif 'vol' in tag:
            for filename in filenames:
                if 'zip' in filename:
                    new_tag = tag.split('vol')[1]
                    if new_tag+'.zip' == filename or new_tag+'_.zip' == filename:
                        dic_of_docs[tag] = filename
                        print('!', filename)
        else:
            print('BAD!', tag)
    path_to_file = os.path.dirname(os.path.realpath(__file__)) + "/xml_data/"
    my_file = open(path_to_file+dic_of_docs[tag], 'r')
    response = HttpResponse(my_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % dic_of_docs[tag]
    return response

def simple_search(request):
    print('!!!')
    if request.method == "POST":
        simple_search = request.POST.get('search_input')
        print(simple_search)
        data = [[]]
        return render(request, 'text_search_out.html', {'res_data': data})


def query_process(request):
    """
    Process query and return string of Query and results objects
    :param request:
    :return: query_out - string,
    """
    whole_query = {}
    place = request.POST.get('place')
    finish = request.POST.get('finish')
    year = request.POST.getlist('year')
    century = request.POST.getlist('century')
    sphere = request.POST.getlist('sphere')
    edit = request.POST.get('edit')
    cycle = request.POST.get('cycle')
    type = request.POST.getlist('type')
    volum = request.POST.getlist('volum')

    whole_query[u"Место"] = (place,'place')
    whole_query[u'Законченность'] = (finish, 'finish')
    whole_query[u'Время написания'] = (year, 'year')
    whole_query[u'Время повествования'] = (century, 'century')
    whole_query[u'Сфера'] = (sphere, 'sphere')
    whole_query[u'Изданное'] = (edit, 'edit')
    whole_query[u'Цикл'] = (cycle, 'cycle')
    whole_query[u'Тип'] = (type, 'type')
    whole_query[u'Том'] = (volum, 'volum')

    query_out = []
    for key, value in whole_query.items():
        if isinstance(value[0], list):
            if value[0] == []:
                new_value = '- '
            else:
                new_value = ' '.join(value[0])
            query_out.append(key + ': ' + new_value)
        else:
            if value[0] == 'none':
                new_value = '- '
            else:
                new_value = value[0]
            query_out.append(key + ': ' + new_value)
    # Если человек не нажал значит, ему это не интересно. Не смотреть такие случаи вообще
    new_results = Works.objects.all()
    for key, val in whole_query.items():
        if val[0] != 'none' and val[1] == 'place':
            new_results = new_results.filter(place=place)
        elif val[0] != 'none' and val[1] == 'finish':
            new_results = new_results.filter(finished=finish)
        elif val[0] != [] and val[1] == 'year':
            new_results = new_results.filter(date__in=year)
        elif val[0] != [] and val[1] == 'century':
            new_results = new_results.filter(time__in=century)
        elif val[0] != [] and val[1] == 'sphere':
            new_results = new_results.filter(sphere__in=sphere)
        elif val[0] != 'none' and val[1] == 'edit':
            new_results = new_results.filter(edited=edit)
        elif val[0] != [] and val[1] == 'type':
            new_results = new_results.filter(type__in=type)
        elif val[0] != 'none' and val[1] == 'cycle':
            new_results = new_results.filter(cycle=cycle)
        elif val[0] != [] and val[1] == 'volum':
            new_results = new_results.filter(value__in=volum)
    return '; '.join(query_out), new_results


def parse_xml_doc(new_path, query):
    query_paragraphs = []
    pages = []
    with codecs.open(new_path, 'r') as one_doc:
        xml_document = one_doc.read()
        soup = BeautifulStoneSoup(xml_document, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        paragraphs = soup.findAll('p')
        for par in paragraphs:
            if query in par.contents[0]:
                query_paragraphs.append(par.contents[0])
                my_page = par.find('span',{"class": "opnumber"})
                if my_page != None:
                    pages.append(my_page.contents[0])
    return query_paragraphs, pages

def search_in_current_docs(docs, text_query):
    """We have a set of documents in which to find text.
    Parse only these docs and catch the text"""
    results = []
    all_items = 0
    for doc in docs:
        for root, dirs, filenames in os.walk(os.getcwd() + '/leo_tolstoy/xml_data/'):
            for fname in filenames:
                if doc.filename == fname:
                    new_path = os.path.join(root, fname)
                    my_doc, pages = parse_xml_doc(new_path, text_query)
                    if len(my_doc) > 0:
                        length = len(my_doc)
                        paragraph = my_doc[-1]
                        all_items += length
                        cite = u'"'+doc.name + u'. "' + doc.source[:-1] + u', стр. ' + pages[-1]
                        results.append((doc.name, paragraph, doc.value, cite))
    return results, all_items

def search_big(request):

    if request.method == "POST":

        query_out, docs = query_process(request)
        text_query = request.POST.get('search_big_input')
        if text_query:
            print('BIG search')
            results, all_count = search_in_current_docs(docs, text_query)
            return render(request, 'text_search_out.html', {'res_docs': results,
                                                            'match': all_count,
                                                            'len': len(results),
                                                            'query': query_out})
        else:
            print('Meta search!')
            return render(request, 'meta_search_out.html', {'res_docs': docs,
                                                            'query': query_out,
                                                            'len': len(docs)})
