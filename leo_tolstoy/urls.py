from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'data$', views.show_data, name='show_data'),
    url(r'search$', views.start_search, name='search_main'),

    url(r'^data/download/(?P<tag>.+)/$', views.all_files_download, name='files_download'),
]