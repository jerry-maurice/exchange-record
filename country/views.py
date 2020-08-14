from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from country.models import Country
from employee.models import  Employee
from account.models import Account
from company.models  import Company, Location

import logging, requests, json

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


@login_required
def addCountry(request):
    '''
    add countries
    '''
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        if request.method == 'GET':
            countries =  Country.objects.filter(company=company)
            context = {
                'countries':countries,
                'company':company,
            }
            return  render(request,  'country/add/countryadd.html',context)
        if request.method == 'POST':
            try:
                json_data = json.loads(request.body)
                name = json_data['name']
                alpha2Code = json_data['alpha2Code']
                alpha3Code = json_data['alpha3Code']
                currency = json_data['currency']
                flag = json_data['flag']
                language = json_data['language']
                country = Country(name=name, alpha2Code=alpha2Code, alpha3Code=alpha3Code, 
                currency=currency, flag=flag, language=language, company=company)
                country.save()
            except json.decoder.JSONDecodeError:
                logger.warning("String could not be converted to JSON")
            return redirect(addCountry)
    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)
    