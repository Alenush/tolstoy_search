#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
from BeautifulSoup import BeautifulStoneSoup
from django.http import JsonResponse
import pymorphy2

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import codecs
import sys
import pprint
from string import punctuation

streamWriter = codecs.lookup('utf-8')[-1]
sys.stdout = streamWriter(sys.stdout)

analyzer = pymorphy2.MorphAnalyzer()

from leo_tolstoy.models import OriginalWorks, TeiWorks
from leo_tolstoy.models import MyUser, TolstoyTexts
from leo_tolstoy.models import index_data


def index(request):
    return render(request, 'index.html')

def show_data(request):
    all_works = TeiWorks.objects.all()
    paginator = Paginator(all_works, 20)
    page = request.GET.get('page')
    try:
         my_works = paginator.page(page)
    except PageNotAnInteger:
        my_works = paginator.page(1)
    except EmptyPage:
        my_works = paginator.page(paginator.num_pages)
    return render(request, 'data.html', {"works":my_works, 'volums':[], 'check':1})

def show_chudozh(request):
    chudozh = set()
    for works in TeiWorks.objects.filter(sphere='художественная'):
        chudozh.add(works)
    paginator = Paginator(list(chudozh), 20)
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
    for works in TeiWorks.objects.all():
        volums.add(works.value)
    return render(request, 'data.html', {"works": [], 'volums': volums})

def show_public(request):
    public = set()
    for works in TeiWorks.objects.filter(sphere='публицистика'):
        public.add(works)
    paginator = Paginator(list(public), 20)
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
    for works in TeiWorks.objects.filter(sphere='дневники и записные книжки'):
        diaries.add(works)
    return render(request, 'data.html', {"works": diaries})

def show_letters(request):
    letters = set()
    for works in TeiWorks.objects.filter(sphere='Личная и деловая переписка'):
        letters.add(works)
    # paginator = Paginator(list(letters), 20)
    # page = request.GET.get('page')
    # try:
    #     letters_works = paginator.page(page)
    # except PageNotAnInteger:
    #     letters_works = paginator.page(1)
    # except EmptyPage:
    #     letters_works = paginator.page(paginator.num_pages)
    return render(request, 'data.html', {"works": letters})

def show_children(request):
    children = set()
    for works in TeiWorks.objects.filter(sphere='детская литература'):
        children.add(works)
    return render(request, 'data.html', {"works": children})

def show_church(request):
    church = set()
    for works in TeiWorks.objects.filter(sphere='Церковно-богословская литература'):
        church.add(works)
    return render(request, 'data.html', {"works": church})

def find_doc(request):
    search_works = set()
    if request.method == "POST":
        query = request.POST.get('query')
        for works in TeiWorks.objects.filter(name__contains=query.upper()):
            search_works.add(works)
    return render(request, 'data.html', {"works": search_works})

def start_search(request):
    vol_array = range(1,91)
    years = set()
    for works in OriginalWorks.objects.all():
        if works.date != None and works.date != '?' and works.date!='0':
            if type(works.date)!='unicode':
                years.add(works.date)
    return render(request, 'search.html', {'vol_array':vol_array, 'years': sorted(years)})

def redirect_to_html(request, link):
    return render(request, link, {})


def all_files_download(request, tag):
    """
    Download xml files
    :param tag: all, vol_n, file
    """
    dic_of_docs = {'all':'tei_data.zip'}
    for folder in os.listdir(os.path.realpath(os.getcwd())+'/leo_tolstoy/xml_data/'):
        if folder.endswith('zip'):
            vol = folder.split('.')[0].replace('_','')
            dic_of_docs[vol] = folder
    global path_to_file
    for root, dirs, filenames in os.walk(os.getcwd()+'/leo_tolstoy/xml_data/'):
        if 'xml' in tag:
            for filename in filenames:
                if os.path.split(filename)[-1].decode('utf-8') == tag:
                    new_path = os.path.join(root, filename)
                    new_tag = new_path.split('/')[-2:]
                    dic_of_docs[tag] = '/'.join(new_tag)
    path_to_file = os.path.dirname(os.path.realpath(__file__)) + "/xml_data/"
    my_file = open(path_to_file+dic_of_docs[tag], 'r')
    response = HttpResponse(my_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % dic_of_docs[tag]
    return response

def query_process(request, source=OriginalWorks):
    """
    Process query and return string of Query and results objects
    :return: query_out - string,
    """
    whole_query = {}
    place = request.POST.get('place')
    finish = request.POST.get('finish')
    orpho = request.POST.get('orpho')
    year = request.POST.getlist('year')
    century = request.POST.getlist('century')
    sphere = request.POST.getlist('sphere')
    edit = request.POST.get('edit')
    cycle = request.POST.get('cycle')
    type = request.POST.getlist('type')
    volum = request.POST.getlist('volum')

    whole_query[u"Место"] = (place,'place')
    whole_query[u'Законченность'] = (finish, 'finish')
    whole_query[u'Орфография'] = (orpho, 'orpho')
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
    new_results = source.objects.all()
    for key, val in whole_query.items():
        if val[0] != 'none' and val[1] == 'place':
            new_results = new_results.filter(place=place)
        elif val[0] != 'none' and val[1] == 'finish':
            new_results = new_results.filter(finished=finish)
        elif val[0] != 'none' and val[1] == 'orpho':
            new_results = new_results.filter(orpho=orpho)
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
                my_page = par.find('span', {"class": "opnumber"})
                if my_page != None:
                    pages.append(my_page.contents[0])
    return query_paragraphs, pages


def find_lemmas_docs(lemmas):
    """
    Takes lemmas. check in db the lists of documents that satisfied the query.
    Cross these sets. Return the documents objects that satisfied the whole query.
    :param lemmas: array of lemmas from the query
    :return: array of documents (path|page|par).
    """
    sets = []
    for lemma in lemmas:
        one_lemma_set = set()
        documents = index_data[lemma] # dictionary
        for doc, page_dic in documents.items():
            for page, par in page_dic.items():
                one_lemma_set.add(u"{}|{}|{}".format(doc, page, par))
        sets.append(one_lemma_set)
    current_set = sets[0]
    for one_set in sets[1:]:
        my_set = current_set & one_set
        current_set = my_set
    print("RESULTS", len(current_set))
    return current_set

def filtered_docs_search(request, lemmas): #NEED TO CHECK
    valid_docs = find_lemmas_docs(lemmas)
    query, filters_works = query_process(request, source=TeiWorks)

    results = []
    for filt_doc in filters_works:
        for path_doc in valid_docs:
            filename = path_doc.split('|')[0]
            if filt_doc.filename == filename:
             results.append(path_doc)
    return results, query

def search_big(request):

    if request.method == "POST":
        text_query = request.POST.get('search_big_input')
        if text_query:
            words = [word.strip(punctuation + '- ').lower() for word in text_query.split() if word != '']
            lemmas = [analyzer.parse(word)[0].normal_form for word in words]
            valid_docs, query_out = filtered_docs_search(request, lemmas)
            snippets = [take_data_from_lemma(doc) for doc in valid_docs]
            return render(request, 'text_search_out.html', {'res_docs': snippets,
                                                                'match': len(snippets),
                                                                'len': len(valid_docs),
                                                                'query': query_out})
        else:
            query_out, docs = query_process(request, source=OriginalWorks)
            if request.POST.get('format') == 'meta':
                print('Meta search!')
                return render(request, 'meta_search_out.html', {'res_docs': docs,
                                                                'query': query_out,
                                                                'len': len(docs)})
            else:
                return redirect('/tolstoy/search/')

def ajax_test(request):
        email = request.GET.get('email', None)
        print('Ajax', email)
        taken = MyUser.objects.filter(email__iexact=email).exists()
        data = {'is_taken': taken}
        if data['is_taken']:
            data['error_message'] = 'Вы уже писали сообщение. Нам хватит =Р'
        return JsonResponse(data)


def feedback_save(request):
    if request.POST:
        message = request.POST['message']
        email = request.POST['email']
        user_back = MyUser(message=message, email=email)
        user_back.save()
        print("Save object")
        return redirect('/tolstoy/')


def take_data_from_lemma(doc):
    """
    :param doc: path|page|par
    :return: return only the first paragraph with this page
    """
    doc = doc.replace('_NoSameBacknotes','')
    path, page, index = doc.split('|')
    good_objects = TolstoyTexts.objects.filter(filename=path, page=page, par_index=index)
    parag = good_objects[0].paragraphs.replace('$$','\n')
    html_link = good_objects[0].html_link
    tei_doc = TeiWorks.objects.filter(filename=path)
    name = tei_doc[0].name
    volum = tei_doc[0].value
    cite = tei_doc[0].source + page
    return (html_link, name, parag, volum, cite)

def search_lemma(request):
    query_to_search = request.POST.get('search_input', '')
    print("Whole", query_to_search)
    words = [word.strip(punctuation + '- ').lower() for word in query_to_search.split() if word != '']
    lemmas = [analyzer.parse(word)[0].normal_form for word in words]
    documents = find_lemmas_docs(lemmas)
    snippets = [take_data_from_lemma(doc) for doc in documents]
    return render(request, 'text_search_out.html', {'res_docs': snippets,
                                                        'query': query_to_search,
                                                        'len': len(documents)})