#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
import os
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

from leo_tolstoy.models import OriginalWorks, Letters, MyUser, \
    TolstoyTexts, TolstoyLetters, LemmasInverseTable
# from leo_tolstoy.models import index_data, index_data_letters


def index(request):
    return render(request, 'index.html')

def show_data(request):
    all_works = OriginalWorks.objects.all()
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
    for works in OriginalWorks.objects.filter(sphere='художественная'):
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
    for works in OriginalWorks.objects.all():
        volums.add(works.value)
    return render(request, 'data.html', {"works": [], 'volums': volums})

def show_public(request):
    public = set()
    for works in OriginalWorks.objects.filter(sphere='публицистика'):
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

def show_letters(request):
    letters = set()
    for works in Letters.objects.all():
        letters.add(works)
    paginator = Paginator(list(letters), 50)
    page = request.GET.get('page')
    try:
        letters_works = paginator.page(page)
    except PageNotAnInteger:
        letters_works = paginator.page(1)
    except EmptyPage:
        letters_works = paginator.page(paginator.num_pages)
    return render(request, 'data.html', {"works": letters_works,'check':2})

def show_children(request):
    children = set()
    for works in OriginalWorks.objects.filter(sphere='детская литература'):
        children.add(works)
    return render(request, 'data.html', {"works": children})

def show_church(request):
    church = set()
    for works in OriginalWorks.objects.filter(sphere='Церковно-богословская литература'):
        church.add(works)
    return render(request, 'data.html', {"works": church})

def find_doc(request):
    """Search in all tei-documents. Get user query and
     find the documents contained this name"""
    search_works = set()
    if request.method == "POST":
        query = request.POST.get('query')
        for works in OriginalWorks.objects.filter(name__contains=query):
            search_works.add(works)
        for letter in Letters.objects.filter(name__contains=query):
            search_works.add(letter)
    return render(request, 'data.html', {"works": search_works})

def start_search(request):
    """Open search interface. Render all data for template from db"""
    vol_array, years, letter_volumns, letter_ids, addresats, \
    let_place, topics = set(), set(), set(), set(), set(), set(), set()
    for letter in Letters.objects.all():
        letter_volumns.add(letter.value)
        letter_ids.add(letter.number)
        for adres in letter.addressee.split('_'):
            addresats.add(adres)
        let_place.add(letter.place)
    for works in OriginalWorks.objects.all():
        if works.date != None and works.date != '?' and works.date!='0':
            if type(works.date)!='unicode':
                years.add(works.date)
                vol_array.add(works.value)
                if works.topic != None:
                    topics.add(works.topic)
    return render(request, 'search.html', {'vol_array':sorted(vol_array), 'years': sorted(years),
                                           'let_volums': sorted(letter_volumns),
                                           'let_ids':sorted(letter_ids),
                                           'addressats':sorted(addresats),
                                           'let_place':sorted(let_place),
                                           'topics':sorted(topics)})

def redirect_to_html(request, link):
    return render(request, link, {})


def all_files_download(request, tag):
    """
    Download xml files
    :param tag: all, vol_n, file
    """
    dic_of_docs = {'all':'tei_data.zip', 'all_letters':'letters.zip'}
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
                    new_tag = new_path.split('/')[-1:]
                    dic_of_docs[tag] = '/'.join(new_tag)
    path_to_file = os.path.dirname(os.path.realpath(__file__)) + "/xml_data/"
    try:
        my_file = open(path_to_file+dic_of_docs[tag], 'r')
        response = HttpResponse(my_file, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % dic_of_docs[tag]
        return response
    except:
        return redirect('/tolstoy_search/data/') 

def make_query_out(whole_query):
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
    return query_out

def query_process_letters(request):
    """Process the letter query"""
    whole_query = {}
    let_id = request.POST.get('let_id')
    let_place = request.POST.getlist('let_place')
    let_adressat = request.POST.getlist('let_adressat')
    date1 = request.POST.get('date1')
    date2 = request.POST.get('date2')
    let_type = request.POST.getlist('let_type')
    let_volum = request.POST.getlist('let_volum')

    whole_query[u"Место"] = (let_place, 'place')
    whole_query[u'Номер'] = (let_id, 'id_name')
    whole_query[u'Дата начала написания'] = (date1, 'date1')
    whole_query[u'Дата окончания написания'] = (date2, 'date2')
    whole_query[u'Адресат'] = (let_adressat, 'adressat')
    whole_query[u'Тип'] = (let_type, 'type')
    whole_query[u'Том'] = (let_volum, 'volum')

    query_out = make_query_out(whole_query)
    # Если человек не нажал значит, ему это не интересно. Не смотреть такие случаи вообще
    new_results = Letters.objects.all()
    for key, val in whole_query.items():
        if val[0] != ['none'] and val[1] == 'place':
            new_results = new_results.filter(place=let_place[0])
        elif val[0] != '' and val[1] == 'id_name':
            new_results = new_results.filter(number=let_id)
        elif val[0] != '' and (val[1] == 'date1' or val[1] == 'date2'):
            new_results = new_results.filter(date1__range=(date1,date2)) # date2 в базе не учитывается по сути. а надо?
        elif val[0] != ['none'] and val[1] == 'adressat':
            new_results = new_results.filter(addressee__contains=let_adressat[0])
        elif val[0] != ['none'] and val[1] == 'type':
            new_results = new_results.filter(type=let_type[0])
        elif val[0] != [] and val[1] == 'volum':
            new_results = new_results.filter(value__in=let_volum)

    return '; '.join(query_out), new_results

def query_process_works(request, source=OriginalWorks):
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
    topic = request.POST.getlist('topic')

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
    whole_query[u'Топик'] = (topic, 'topic')

    query_out = make_query_out(whole_query)
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
        elif val[0] != [] and val[1] == 'topic':
            new_results = new_results.filter(topic__in=topic)
    return '; '.join(query_out), new_results

def find_lemmas_docs_all(lemmas):
    """Lemmas from query. Array"""
    sets = []
    for lemma in lemmas:
        one_lemma_set = set()
        valid_documents = LemmasInverseTable.objects.filter(documents=lemma)
        for doc in valid_documents:
            one_lemma_set.add(doc.type)
        sets.append(one_lemma_set)
    current_set = sets[0]
    for one_set in sets[1:]:
        my_set = current_set & one_set
        current_set = my_set
    return current_set

def find_lemmas_docs(lemmas, source='work'):
    """
    Takes lemmas. check in db the lists of documents that satisfied the query.
    Cross these sets. Return the documents objects that satisfied the whole query.
    :param lemmas: array of lemmas from the query
    :return: array of documents (path$page$par).
    """
    sets = []
    for lemma in lemmas:
        one_lemma_set = set()
        valid_documents = LemmasInverseTable.objects.filter(lemma=source).filter(documents=lemma)
        for doc in valid_documents:
            one_lemma_set.add(doc.type)
        sets.append(one_lemma_set)
    current_set = sets[0]
    for one_set in sets[1:]:
        my_set = current_set & one_set
        current_set = my_set
    return current_set

def filtered_docs_search(request, lemmas, source):
    valid_docs = find_lemmas_docs(lemmas, source)
    if source == 'work':
        query, filters_works = query_process_works(request)
    else:
        query, filters_works = query_process_letters(request)
    results = []
    for filt_doc in filters_works:
        for path_doc in valid_docs:
            filename = path_doc.split('$$')[0]
            if filt_doc.filename == filename:
                results.append(path_doc)
    return results, query

def search_big(request):
    """Развернутый поиск. Check if it meta search or text and by letters or works"""
    if request.method == "POST":
        texts_letters = request.POST.get('format')
        if texts_letters == 'letters':
            source, type = Letters, 'letter'
        else:
            source, type = OriginalWorks, 'work'
        text_query = request.POST.get('big_search_query')
        print(text_query)
        if text_query:
            words = [word.strip(punctuation + '- ').lower() for word in text_query.split() if word != '']
            lemmas = [analyzer.parse(word)[0].normal_form for word in words]
            valid_docs, query_out = filtered_docs_search(request, lemmas,type)
            snippets = sorted([take_data_from_lemma(doc, words, source) for doc in valid_docs], key=lambda x: x[3])
            return render(request, 'text_search_out.html', {'res_docs': snippets,
                                                                'match': len(snippets),
                                                                'len': len(valid_docs),
                                                                'query': query_out})
        else:
            if source == OriginalWorks:
                query_out, docs = query_process_works(request)
            else:
                query_out, docs = query_process_letters(request)
            return render(request, 'meta_search_out.html', {'res_docs': docs,
                                                             'query': query_out,
                                                             'len': len(docs)})
    else:
        return redirect('/tolstoy_search/search/')

def bold_lemmas_in_par(par, query_words):
    """
    Make bold query words in snippet
    :return snippet with bold query-words. string
    """
    new_par = []
    query = [w.word.lower() for q_w in query_words for w in analyzer.parse(q_w)[0].lexeme]
    for word in par.split():
        if word.lower() in query or word[:-1] in query:
            word = '<b>'+word+'</b>'
            new_par.append(word)
        else:
            new_par.append(word)
    return ' '.join(new_par)

def take_data_from_lemma(doc, lemmas, type=OriginalWorks):
        """
        :param doc: path|page|par
        :return: return only the first paragraph with this page
        """
        path, page, index = doc.split('$$')
        if type == OriginalWorks:
            good_objects = TolstoyTexts.objects.filter(filename=path, page=page, par_index=index)
        else:
            good_objects = TolstoyLetters.objects.filter(filename=path, page=page, par_index=index)

        parag = good_objects[0].paragraphs.replace('$$', '\n')
        if len(parag.split()) >= 100:
            parag = ' '.join(parag.split()[:100]) + '...'
            parag = bold_lemmas_in_par(parag, lemmas)
        else:
            parag = bold_lemmas_in_par(parag, lemmas)
        html_link = good_objects[0].html_link + '#'+page+'_'+index
        tei_doc = type.objects.filter(filename=path)
        name = tei_doc[0].name
        volum = tei_doc[0].value
        cite = tei_doc[0].source[:-1] + u', стр. ' + page
        return (html_link, name, parag, volum, cite, index)

def take_data_from_lemma_all(doc, words):
    path, page, index = doc.split('$$')
    good_objects1 = TolstoyTexts.objects.filter(filename=path, page=page, par_index=index)
    good_objects2 = TolstoyLetters.objects.filter(filename=path, page=page, par_index=index)
    if len(good_objects1) != 0:
        parag = good_objects1[0].paragraphs.replace('$$', '\n')
        html_link = good_objects1[0].html_link + '#' + page + '_' + index
    else:
        parag = good_objects2[0].paragraphs.replace('$$', '\n')
        html_link = good_objects2[0].html_link + '#' + page + '_' + index
    if len(parag.split()) >= 100:
        parag = ' '.join(parag.split()[:100]) + '...'
        parag = bold_lemmas_in_par(parag, words)
    else:
        parag = bold_lemmas_in_par(parag, words)

    tei_doc_works = OriginalWorks.objects.filter(filename=path)
    tei_docs_letters = Letters.objects.filter(filename=path)
    if len(tei_doc_works) != 0:
        name = tei_doc_works[0].name
        volum = tei_doc_works[0].value
        cite = tei_doc_works[0].source[:-1] + u', стр. ' + page
    elif len(tei_docs_letters) != 0:
        name = tei_docs_letters[0].name
        volum = tei_docs_letters[0].value
        cite = tei_docs_letters[0].source[:-1] + u', стр. ' + page
    else:
        return None
    return (html_link, name, parag, volum, cite, index)

def search_lemma(request):
        query_to_search = request.POST.get('search_input', '')
        if query_to_search:
            words = [word.strip(punctuation + '- ').lower() for word in query_to_search.split() if word != '']
            lemmas = [analyzer.parse(word)[0].normal_form for word in words]
            documents = find_lemmas_docs_all(lemmas)
            snippets = []
            for doc in documents:
                results = take_data_from_lemma_all(doc, words)
                if results!=None:
                    snippets.append(results)
            snippets = sorted(snippets, key=lambda x: x[3])
            return render(request, 'text_search_out.html', {'res_docs': snippets,
                                                            'query': query_to_search,
                                                            'len': len(documents)})
        else:
            return redirect('/tolstoy_search/search/')

#================For Ajax. User feedback. ===============

def ajax_test(request):
        email = request.GET.get('email', None)
        print('Ajax', email)
        taken = MyUser.objects.filter(email__iexact=email).exists()
        data = {'is_taken': taken}
        if data['is_taken']:
            data['error_message'] = 'Вы уже писали сообщение. Но мы рады улышать вас снова!'
        return JsonResponse(data)

def feedback_save(request):
    if request.POST:
        message = request.POST['message']
        email = request.POST['email']
        user_back = MyUser(message=message, email=email)
        user_back.save()
        print("Save object")
        return redirect('/tolstoy_search/')

