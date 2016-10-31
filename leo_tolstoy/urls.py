from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'data/$', views.show_data, name='show_data'),
    url(r'^search/$', views.start_search, name='search_main'),

    url(r'^searching/$', views.search_big, name='all_search'),
    url(r'^simple_search/$', views.search_lemma, name='main_search'),

    url(r'data/volums/$', views.show_volums, name='volums'),
    url(r'data/public/$', views.show_public, name='public'),
    url(r'data/diaries/$', views.show_diaries, name='diaries'),
    url(r'data/letters/$', views.show_letters, name='letters'),
    url(r'data/children/$', views.show_children, name='children'),
    url(r'data/church/$', views.show_church, name='church'),
    url(r'data/chud/$', views.show_chudozh, name='chud'),

    url(r'data/result/$', views.find_doc, name='find_doc'),

    url(r'data/download/(?P<tag>.+)/$', views.all_files_download, name='files_download'),
    url(r'result/doc/(?P<link>.+)/$', views.redirect_to_html, name='redirect'),

    url(r'^ajax/ajax_test/$', views.ajax_test, name='ajax_call'),
    url(r'^/$', views.feedback_save, name='feedback'),
]