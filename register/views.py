from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from  employee.models import Employee
from register.models import  Register, Register_Status, RegisterAssigned, Register_Log
from account.models import Account
from company.models import Company, Location
from country.models import  Country
from fund.models import Fund, FundTransaction

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
    

@login_required
def assign_register(request, emp_id):
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        employee = get_object_or_404(Employee, id=emp_id)
        assigned = RegisterAssigned.objects.filter(employee=employee, date=date.today())
        register = Register.objects.filter(company=company)
        if request.method == 'GET':
            context = {
                'assigned':assigned,
                'company':company,
                'employee':employee,
                'today':date.today(),
                'register':register
            }
            return render(request, 'register/add/assignRegister.html', context)
        if request.method == 'POST':
            cash_register = get_object_or_404(Register, id=request.POST['register']) 
            assignRegister = RegisterAssigned(employee=employee, register=cash_register, date=date.today())
            assignRegister.save()
            return redirect(assign_register, employee.id)
    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)


@login_required
def remove_assign_register(request,emp_id, register_id ):
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        if request.method == 'GET':
            employee = get_object_or_404(Employee, id=emp_id)
            register = get_object_or_404(Register, id=register_id)
            assigned = get_object_or_404(RegisterAssigned, employee=employee, register=register, date=date.today())
            assigned.delete()
            return redirect(assign_register, employee.id)
    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)


@login_required
def register_operation(request, register_id):
    '''
    deposit and withdraw money in register
    '''
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        register = get_object_or_404(Register, id=register_id)
        fund  = get_object_or_404(Fund, country=register.country, company=company)
        if request.method == 'GET':
            context ={
                'company':company,
                'register':register,
                'fund':fund,
            }
            return render(request, 'register/operation/operation.html',context)
        if request.method == 'POST':
            operationType = request.POST['type']
            amount = request.POST['amount']
            previous_amount = fund.funds
            register_previous_amount = register.balance
            source = ""
            actual_balance = 0
            source = "Register"
            if operationType == '1':
                actual_balance = float(previous_amount) - float(amount)
                register_balance =  float(register_previous_amount) + float(amount)
                logger.info(actual_balance)
                if  actual_balance < 0:
                    context = {
                        'message':'Low in fund. Transaction can\'t be completed'
                    }
                    return render(request, 'account/message/message.html',context)
                else:
                    fund.funds = actual_balance
                    fund.save()
                    transaction = FundTransaction(withdrew=amount, previous_balance=previous_amount, 
                                actual_balance=actual_balance, source=source, fund=fund)
                    transaction.save()
                    register.balance  = register_balance
                    register.save()
                    log = Register_Log(actual_balance=register_balance, deposited=amount,  previous_balance=register_previous_amount, register=register)
                    log.save()
            elif operationType == '0':
                actual_balance = float(previous_amount) + float(amount)
                register_balance =  float(register.balance) - float(amount)
                fund.funds = actual_balance
                fund.save()
                transaction = FundTransaction(deposited=amount, previous_balance=previous_amount, 
                            actual_balance=actual_balance, source=source, fund=fund)
                transaction.save()
                register.balance  = register_balance
                register.save()
                log = Register_Log(actual_balance=register_balance, withdrew=amount,  previous_balance=register_previous_amount, register=register)
                log.save()
            return redirect(registerAdminList)
    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)


@login_required
def log_display(request, register_id):
    '''
    return the list of transactions
    '''
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        if request.method == 'GET':
            register = get_object_or_404(Register, id=register_id)
            logs = Register_Log.objects.filter(register=register)
            context = {
                'logs':logs,
                'company':company,
            }
            return render(request,'register/log/log.html',context)
    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)
