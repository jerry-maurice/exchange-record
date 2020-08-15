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
        countries =  Country.objects.filter(company=company)
        if request.method == 'GET':
            context = {
                'countries':countries,
                'company':company,
            }
            return  render(request,  'country/add/countryadd.html',context)
        if request.method == 'POST':
            country_name =  request.POST['country']
            search_url = 'https://restcountries.eu/rest/v2/name/'+country_name
            response = requests.get(search_url)
            if response.status_code == 200:
                data = response.json()
                name = data[0]['name']
                alpha2Code = data[0]['alpha2Code']
                alpha3Code = data[0]['alpha3Code']
                currency = data[0]['currencies'][0]['name']
                symbol = data[0]['currencies'][0]['symbol']
                flag = data[0]['flag']
                language = data[0]['languages'][0]['nativeName']
                if Country.objects.filter(name=name, company=company).exists() == False:
                    country = Country(name=name, alpha2Code=alpha2Code, alpha3Code=alpha3Code, 
                                currency=currency, flag=flag, language=language, company=company)
                    country.save()
            else:
                context = {
                    'countries':countries,
                    'company':company,
                    'message':'The country that you specified was not found'
                }
                return  render(request,  'country/add/countryadd.html',context)
            return redirect(addCountry)
            '''try:
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
            return redirect(addCountry)'''
    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)
    