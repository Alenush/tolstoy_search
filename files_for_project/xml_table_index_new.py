import winsound
from bs4 import BeautifulSoup
import bs4
from pprint import pprint as pp
import sqlite3
import sqlite3
from pymorphy2 import MorphAnalyzer
import os
from collections import OrderedDict, defaultdict
import pandas
import re
from string import punctuation
import json


class ParseTei:
    def __init__(self, tei_data_path):
        """
        :param data_base_path: путь к базе данных
        :param tei_data_path: путь к папке с файлами в разметке TEI
        """
        self.files = [os.path.join(*list(os.path.split(tei_data_path)) + [filename])
                      for filename in os.listdir(tei_data_path)]

        self.file_metadata = {}  # словарь с метаданными
        self.file_text_data = defaultdict(lambda: defaultdict(str))  # словарь с данными по каждой странице и каждому абзацу
        self.file_html_data = ''  # словарь, в котором хранятся данные в формате html для каждой страницы
        self.inverted_index = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))  # обратный индекс

        self.xml_text = []
        self.current_page_id = 0
        self.current_par_id = 0
        self.current_file = ''
        self.preprocessing_regex = re.compile('[\r\n\t ]')
        self.pymorphy = MorphAnalyzer()
        self.reg = re.compile('\n+| {2,}')

    @staticmethod
    def parse_xml(xml_file_path):
        """
        Читает файл по указанному пути, парсит и возвращает объект BeautifulSoup
        :param xml_file_path: Путь к файлу XML
        :return: объект Soup
        """
        with open(xml_file_path, 'r', encoding='utf-8') as f:
            return BeautifulSoup(f.read(), 'xml')

    def get_metadata(self, bs_xml_data):
        """
        Парсит полученные данные XML (пропущенные через Beautiful soup) и вытаскивает метаданные
        :param bs_xml_data: BeautifulSoup object
        :return: словарь с метаданными
        """
        self.file_metadata = OrderedDict()

        metadata_element = bs_xml_data.find('filedesc')
        self.file_metadata['value'] = metadata_element.find('biblscope', unit='vol').string.strip()
        self.file_metadata['author'] = "Л. Н. Толстой"
        self.file_metadata['name'] = metadata_element.select("titlestmt title")[0].string.strip()
        self.file_metadata['date'] = bs_xml_data.select("profiledesc creation date")[0].string.strip()
        _place = bs_xml_data.select("profiledesc creation rs")
        if _place:
            self.file_metadata['place'] = _place[0]['type']
        else:
            self.file_metadata['place'] = bs_xml_data.select("profiledesc creation placename")[0].string.strip()
            self.file_metadata['time'] = ''
            self.file_metadata['sphere'] = bs_xml_data.select("profiledesc textclass catref[type=sphere]")[0]['target'].strip().replace(
            '#', '')
        _type = bs_xml_data.select("profiledesc textclass catref[type=type]")[0]['target'].strip().replace('#', '')
        self.file_metadata['type'] = _type.split('.')[1]
        self.file_metadata['dop'] = ''
        self.file_metadata['cycle'] = ''
        self.file_metadata['finished'] = ''
        self.file_metadata['edited'] = ''
        self.file_metadata['fin_ver'] = ''
        self.file_metadata['orpho'] = ''
        self.file_metadata['source'] = ''

    @staticmethod
    def get_start_page_num(bs_xml_data):
        """
        Находит на странице XML первое вхождение номера страницы и возвращет его
        :param bs_xml_data: BeautifulSoup object
        :return: int: Номер страницы
        """
        if bs_xml_data.find('pb'):
            return int(bs_xml_data.find('pb')['n'])
        return 1

    def check_page_number(self, element):
        """
        Проверяет, содержит ли элемент номер страницы. Если это номер страницы и он больше чем нынешний,
        изменяет нынешний номер на найденный, завершает текущий парагаф в self.file_text_data и в self.file_html_data,
        добавляет начальные строки для новой страницы в self.file_html_data.
        Если элемент не содержит номера страницы, записывает текст элемента к текущему параграфу.

        :param element: bs element with tag.name "hi"
        :return:
        """
        elt_str_stripped = element.string.strip().replace('\n', '')
        if elt_str_stripped.isnumeric():  # Если цифра, значит это номер страницы
            if int(elt_str_stripped) - self.current_page_id == 1:
                self.file_html_data[self.current_page_id] += '</p>'
                self.file_html_data[self.current_page_id] += '{% endblock %}{% endblock %}'
                self.current_page_id = int(elt_str_stripped)  # Переходим на следующую страницу
                self.current_page_id = int(elt_str_stripped)  # Переходим на следующую страницу
                self.current_par_id = 0
                self.file_html_data[self.current_page_id] += '{% extends "output_result.html" %}' \
                                                             '{% block content %}{% load staticfiles %}' \
                                                             '<div class="doc_results"> <p>'
        else:  # Если не цифра - значит кусочек текста прямо перед или после номера страницы
            self.file_text_data[self.current_page_id][self.current_par_id] += elt_str_stripped.rstrip()
            self.file_html_data[self.current_page_id] += element.string

    def end_page(self, pb_element):
        n = int(pb_element['n'])
        if n == self.current_page_id:
            page_par = str(n+1) + '_' + str(0)
            self.file_html_data += '</p><p class="page_num" id="{}">{}</p><hr><p id="{}">'.format(n, n, page_par)
            self.current_page_id = n + 1  # Переходим на следующую страницу
            self.current_par_id = 0

    def make_prerevolutionary_html(self, element):
        """
        Получает элемент типа choice, содержащий написангие слова в современной и дореволюционной орфографиях.
        Создает из него строку html, где современный вариант показан, а дореволюционный скрыт классом hidden.
        :param element: bs element with tag.name "choice"
        """
        if element.find('reg'):
            reg = element.find('reg').string
            orig = element.find('orig').string
            return reg, '<span class="reg">{}</span><span class="orig hidden"> {} </span>'.format(reg, orig)
        else:
            corr = element.find('corr').string
            return corr, corr

    def make_note(self, element):
        note = self.reg.sub(' ', self.reg.sub(' ', element.find('p').get_text()))
        return '', '<span class="note hidden">{}</span>'.format(note)

    @staticmethod
    def path_find(xml, path):
        result = xml.select(path)
        if result:
            return result[0]
        return None

    @staticmethod
    def is_large_section(tag):
        """Находит тэлементы дерева содержащие большой section"""
        if tag.has_attr('type'):
            if tag['type'] == 'section':
                if tag.has_attr('xml:id'):
                    if not tag['xml:id'].startswith('n'):
                        return 1
                else:
                    return 1

    @staticmethod
    def is_poem_section(tag):
        return tag.has_attr('type') and tag['type'] == 'section' and not tag.has_attr('xml:id')

    def get_sections(self, xml_data):
        textclass = self.path_find(xml_data, 'textClass catRef[type="type"]')
        if textclass and textclass['target'].endswith('поэзия'):
            sections = self.xml_text.find_all(self.is_poem_section)
            if not sections:
                sections = self.xml_text.find_all('div', type='stanza')
            return sections
        else:
            sections = self.xml_text.find_all(self.is_large_section)
            if sections:
                return sections
            return [self.xml_text]

    def add_data(self, text, html):
        self.file_text_data[self.current_page_id][self.current_par_id] += text
        self.file_html_data += html

    def add_header(self, section):
        header = section.find('head')
        if header:
            self.add_data('', '<h2>')
            for element in header.contents:
                self.add_element(element)
            self.add_data('', '</h2>')

    def add_element(self, element):
        """
        Добавляет элемент параграфа в данные. Попутно добавляет и обновляет номера страницы, заметки, переносы строк,
        дореволюционную орфографию.
        :param element:
        :return:
        """

        if isinstance(element, bs4.element.Tag):
            if element.name in ['figure', 'graphic', 'add', 'del']:
                pass
            elif element.name in ['hi', 'ref']:
                for element in element.contents:
                    self.add_element(element)
            elif element.name == 'lb':
                self.add_data('\n', '\n')
            elif element.name == 'choice':  # Проверяем на дореволюционную орфографию
                self.add_data(*self.make_prerevolutionary_html(element))
            elif element.name in 'pb':  # Проверяем на номер страницы
                self.end_page(element)
            elif element.name == 'note':  # Проверяем является ли элемент заметкой
                self.add_data(*self.make_note(element))
            else:
                try:
                    self.add_data(element.string, element.string)
                except Exception as e:
                    print('==========!!!!', e, element)
                    raise e

        else:
            self.add_data(element.string, element.string)

    @staticmethod
    def is_paragraph(element):
        """Проверяет, является ли элемент нужным нам параграфом"""
        return element.name == 'p' and not element.find_parents(["note", "del", "add"])

    def add_paragraph(self, p):
        page_par = str(self.current_page_id) + '_' + str(self.current_par_id)  # Номемр страницы + id параграфа на ней.
        if p.has_attr('rend'):  # Если есть форматирование, добавляем его в качестве класса
            self.file_html_data += '<p class="{}" id="{}">'.format(p['rend'], page_par)  # Открываем тэг параграфа
        else:
            self.file_html_data += '<p id="{}">'.format(page_par)
        for element in p.contents:  # Проходим по всем детям элемента и добавляем
            self.add_element(element)
        self.file_html_data += '</p>'  # Закрываем тэг параграфа
        self.current_par_id += 1  # Обновляем индекс

    def initialize_doc(self, xml_data):
        # Словарь с данными по каждой странице и каждому абзацу
        self.file_text_data = defaultdict(lambda: defaultdict(str))
        self.xml_text = xml_data.find('text')
        self.current_page_id = self.get_start_page_num(self.xml_text)
        self.current_par_id = 0
        self.file_html_data = '{% extends "output_result.html" %}' \
                              '{% block content %}{% load staticfiles %}' \
                              '<div class="doc_results">'  # Начальные строки для шаблона html
    # =================================================================================================
    # =================================================================================================

    def update_text_html_index(self, xml_data):
        """
        Добавляет полученные данные из файла во все таблицы: данные о параграфах, данные html, обратный индекс
        :param xml_data: BeautifulSoup object
        """
        self.initialize_doc(xml_data)
        sections = self.get_sections(xml_data)
        for section in sections:  # Проходим по всем разделам текста
            self.add_header(section)  # Выделяем заголовок раздела
            for p in section.find_all(self.is_paragraph):  # Проходим по всем параграфам
                self.add_paragraph(p)  # Добавляем их в данные
        self.file_html_data += '</div>{% endblock %}'  # Закрываем щаблон html

    def make_metadata_table(self, output_path):
        data = []
        metadata = dict()
        for file_path in self.files:
            self.current_file = os.path.split(file_path)[-1].split('.')[0]
            print(self.current_file)
            metadata = self.get_metadata(self.parse_xml(file_path))
            data.append([os.path.split(file_path)[-1]] + list(metadata.values()))
            for page, html in self.file_html_data.items():
                with open(os.path.join('.', 'htmls', self.current_file + '_' + str(page) + '.html'), 'w', encoding='utf-8') as f:
                    f.write(html)
        colnames = metadata.keys()
        pandas.DataFrame(data, columns=['filename'] + list(colnames)).to_csv(output_path, index=True)

    def preprocess_text(self, text):
        """ Токенизирует текс и возвращает список лемм"""
        words = [word.strip(punctuation + '- ').lower() for word in self.preprocessing_regex.split(text) if word != '']
        lemmas = [self.pymorphy.parse(word)[0].normal_form for word in words]
        return [lemma for lemma in lemmas if lemma != '']

    def add_to_inverted_index(self, doc_name, page_num, paragraph_id, paragraph_text):
        """Добавляет текст в обратный индекс"""
        for lemma in self.preprocess_text(paragraph_text):
            if page_num not in self.inverted_index[lemma][doc_name]:
                self.inverted_index[lemma][doc_name][page_num] = paragraph_id

    def make_contents_table(self, contents_output_path, html_output_dir):
        """
        парсит все файлы и добавляет данные в таблицу с полями:
        ["id", "filename", "page", "par_index", "paragraphs", "html_link"]
        Так же добавялет записи в обратный индекс
        :param contents_output_path: путь для сохранения талицы в формате csv
        """
        if not os.path.isdir(html_output_dir):
            os.mkdir(html_output_dir)
        length = len(self.files)
        with open(contents_output_path, 'w', encoding='utf-8') as f:
            f.write('@@'.join(["id", "filename", "page", "par_index", "paragraphs", "html_link"]) + '\n')
            id = 0
            for doc_id, file_path in enumerate(self.files):
                if doc_id % 50 == 0:
                    print(length - doc_id, 'files left')
                self.current_file = os.path.split(file_path)[-1]
                try:
                    self.update_text_html_index(self.parse_xml(file_path))
                except Exception as e:
                    print(print(file_path), 'caused exception', e)
                    winsound.MessageBeep()
                else:
                    html_path = os.path.join(html_output_dir, self.current_file.strip('.xml') + '.html')
                    with open(html_path, 'w', encoding='utf-8') as p:
                        p.write(self.file_html_data)
                    for page_num, pars in sorted(self.file_text_data.items(), key=lambda x: x[0]):
                        for par, text in pars.items():
                            output_data = [id, self.current_file, page_num, par, text.replace('\n', '$$'), html_path]
                            id += 1
                            f.write('@@'.join([str(el) for el in output_data]) + '\n')
                            self.add_to_inverted_index(self.current_file, page_num, par, text)

    def save_inverted_index(self, output_path):
        """Записывает обратный индекс в файл json"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.inverted_index, ensure_ascii=False))

    def get_content_and_index(self, contents_output_path, html_output_dir, index_output_path):
        self.make_contents_table(contents_output_path, html_output_dir)
        self.save_inverted_index(index_output_path)


class ParseLetter(ParseTei):
    def __init__(self, tei_data_path):
        super().__init__(tei_data_path)

    def make_note(self, element):
        self.add_data('', '<span class="note hidden">')
        for element in element.contents:
            self.add_element(element)
        self.add_data('', '</span>')

    @staticmethod
    def get_start_page_num(bs_xml_data):
        """
       Находит на странице XML первое вхождение номера страницы и возвращет его
       :param bs_xml_data: BeautifulSoup object
       :return: int: Номер страницы
       """
        if bs_xml_data.find('hi', style='opnumber'):
            return int(bs_xml_data.find('hi', style='opnumber').string)
        elif bs_xml_data.find('pb'):
            return int(bs_xml_data.find('pb')['n'])
        else:
            return 1

    def end_page(self, element):
        if element.name == 'hi':
            n = int(element.string)
        elif element.name == 'pb':
            n = int(element['n'])
        if n == self.current_page_id:
            page_par = str(n+1) + '_' + str(0)
            self.file_html_data += '</{tag}><{tag} class="page_num" id="{n}">{n}</{tag}><hr><{tag} id="{pp}">'.format(n=n, pp=page_par, tag=self.tag)
            self.current_page_id = n + 1  # Переходим на следующую страницу
            self.current_par_id = 0

    def add_element(self, element):
        """
        Добавляет элемент параграфа в данные. Попутно добавляет и обновляет номера страницы, заметки, переносы строк,
        дореволюционную орфографию.
        :param element:
        """
        if isinstance(element, bs4.element.Tag):
            if element.name in ['figure', 'graphic', 'add', 'del']:
                pass
            elif element.name in ['hi', 'ref']:
                if element.has_attr('style') and element['style'] == 'opnumber':
                    self.end_page(element)
                elif element.has_attr('style') and element['style'] == 'npnumber':
                    pass
                else:
                    for element in element.contents:
                        self.add_element(element)
            elif element.name == 'lb':
                self.add_data('\n', '\n')
            elif element.name in 'pb':  # Проверяем на номер страницы
                self.end_page(element)
            elif element.name == 'choice':  # Проверяем на дореволюционную орфографию
                self.add_data(*self.make_prerevolutionary_html(element))
            elif element.name == 'note':  # Проверяем является ли элемент заметкой
                self.make_note(element)
            else:
                try:
                    self.add_data(element.string, element.string)
                except Exception as e:
                    print('==========!!!!', e, element)
                    raise e
        else:
            self.add_data(element.string, element.string)

    def add_paragraph(self, p):
        self.tag = 'small' if p.parent.name == 'comments' else 'p'
        page_par = str(self.current_page_id) + '_' + str(self.current_par_id)  # Номемр страницы + id параграфа на ней.
        if p.has_attr('rend'):  # Если есть форматирование, добавляем его в качестве класса
            self.file_html_data += '<{} class="{}" id="{}">'.format(self.tag, p['rend'], page_par)  # Открываем тэг параграфа
        else:
            self.file_html_data += '<{} id="{}">'.format(self.tag, page_par)
        for element in p.contents:  # Проходим по всем детям элемента и добавляем
            self.add_element(element)
        self.file_html_data += '</{}>'.format(self.tag)  # Закрываем тэг параграфа
        self.current_par_id += 1  # Обновляем индекс

    def add_header(self, section):
        header = section.find('opener')
        if header:
            self.add_data('', '<h2>')
            for element in header.contents:
                self.add_element(element)
            self.add_data('', '</h2>')

    def initialize_doc(self, xml_data):
        # Словарь с данными по каждой странице и каждому абзацу
        self.file_text_data = defaultdict(lambda: defaultdict(str))
        self.xml_text = xml_data.find('text')
        self.current_page_id = self.get_start_page_num(self.xml_text)
        self.current_par_id = 0
        self.file_html_data = '{% extends "output_result.html" %}' \
                              '{% block content %}{% load staticfiles %}' \
                              '<div class="doc_results">'  # Начальные строки для шаблона html


if __name__ == '__main__':
    # root = 'C:\\alenush\\mariana'
    # root = 'C:\\alenush\\tolstoy\TEI\December_TEI\Final'
    # html_dir = 'C:\\alenush\html_data_2'
    # # test = ParseLetter(root)
    # test = ParseTei(root)
    # # a = test.parse_xml('C:\\alenush\\10_12_2016_person_late\Linked_Person_norm_adresa\Volume_61_D__A__Dyakovu_326.xml')
    # test.get_content_and_index('main2.csv', html_dir, 'main2.json')
    # # test.update_text_html_index(a)
    # # pp(test.file_html_data)
    # # pp(test.file_text_data)
    
    with open('main.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    for lemma,  docs in data.items():
        for doc in docs:
            if doc == "[«Ей, Марьяна, брось работу!..»] 1.xml":
                try:
                    print(lemma)
                    print(data[lemma][doc])
                except UnicodeEncodeError:
                    pass
