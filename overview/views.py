from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# Create your views here.
def index(request):
    '''
    point to the first page of the app
    '''
    return render(request, 'overview/home/index.html')
