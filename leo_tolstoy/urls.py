from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'data$', views.show_data, name='show_data'),
    url(r'search$', views.start_search, name='search_main'),



    url(r'^data/download/(?P<tag>.+)/$', views.all_files_download, name='files_download'),

    url(r'^searching/$', views.search_big, name='all_search'),
    url(r'^simple_search/$', views.simple_search, name='lemma_search'),
]