from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def show_data(request):
    return render(request, 'data.html')

def start_search(request):
    return render(request, 'search.html')

