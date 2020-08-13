from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from country.models import Country
from employee.models import  Employee

import logging

# get an instance of a logger
logger =  logging.getLogger(__name__)

# Create your views here.
@login_required
def countryList(request):
    '''
    list of countries
    '''
    user = request.user
    employee = get_object_or_404(Employee, user=user)
    company = employee.company
    if request.method == 'GET':
        countries = Country.objects.filter(company=company)
        context = {
            'countries':countries,
            'company':company,
        }
        return  render(request,  'country/list/countrylist.html',context)
    