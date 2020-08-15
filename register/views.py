from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from  employee.models import Employee
from register.models import  Register, Register_Status, RegisterAssigned
from account.models import Account
from company.models import Company, Location
from country.models import  Country

import logging
from datetime  import date

# get an instance of a logger
logger =  logging.getLogger(__name__)

# Create your views here.
@login_required
def registerList(request):
    '''
    list of registers appointed to an employee
    '''
    user = request.user
    employee = get_object_or_404(Employee, user=user)
    location = employee.location
    company = employee.company
    '''status = get_object_or_404(Register_Status, name='ACTIVE')'''
    register_assigned = RegisterAssigned.objects.filter(date=date.today(),employee=employee)
    registers = []
    for r in register_assigned:
        registers.append(r.register)
    if request.method == 'GET':
        # registers = Register.objects.filter(company=company,location=location, status=status)
        context = {
            'company':company,
            'register':registers,
        }
        return render(request,'register/list/registerlist.html', context)


@login_required
def registerAdminList(request):
    '''
    list of registers of a company
    '''
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        registers = Register.objects.filter(company=company)
        countries = Country.objects.filter(company=company)
        locations = Location.objects.filter(company=company)
        if request.method == 'GET':
            # registers = Register.objects.filter(company=company,location=location, status=status)
            context = {
                'company':company,
                'register':registers,
                'countries':countries,
                'locations':locations,
            }
            return render(request,'register/list/registerAdminList.html', context)
        if request.method == 'POST': 
            identification = request.POST['identification']
            balance = 0.0
            min_balance = request.POST['min_balance']
            max_balance = request.POST['max_balance']
            location = get_object_or_404(Location, id=request.POST['location'])  
            country = get_object_or_404(Country, id=request.POST['country'])  
            status = get_object_or_404(Register_Status, name='ACTIVE')  
            register = Register(identification=identification, balance=balance, min_balance=min_balance, 
                    max_balance=max_balance, location=location, company=company, country=country, status=status)
            register.save()
            return redirect(registerAdminList)

    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)


@login_required
def registerEmpAssigned(request):
    '''
    list and assign registers
    '''
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        registers_assigned = RegisterAssigned.objects.filter(company=company, date=date.today())
        if request.method == 'GET':
            # registers = Register.objects.filter(company=company,location=location, status=status)
            context = {
                'company':company,
                'register':registers_assigned,
            }
            return render(request,'register/list/registerAssignedList.html', context)

    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)
    