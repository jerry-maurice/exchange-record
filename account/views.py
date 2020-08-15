from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from account.models import Account
from employee.models import Employee
from company.models import Company, Location
from client.models import Client
from sale.models import Order, Product, OrderDetail, Payment, Transaction_Status
from register.models import Register
from country.models import Country

import logging
from datetime import date,  datetime

# get an instance of a logger
logger =  logging.getLogger(__name__)


@login_required
def account_dashboard(request):
    '''
    admin dashboard of the account holder
    '''
    user = request.user
    if request.method == 'GET':
        if Account.objects.filter(user=user).exists():
            account = get_object_or_404(Account, user=user)
            company = get_object_or_404(Company, account=account)
            employees = Employee.objects.filter(company=company)
            clients = Client.objects.filter(company=company)
            today = date.today()
            transaction = Order.objects.filter(location__company=company, placement__gte=today)
            logger.info(today)
            registers = Register.objects.filter(company=company).order_by('balance')[:10]
            product = Product.objects.filter(is_active=True, location__company=company).order_by('-modified')[:10]
            transactions = Order.objects.all().order_by('-placement')[:10]
            countries = Country.objects.filter(company=company)
            context ={
                'employee_size':len(employees),
                'employee':employees,
                'cient':clients,
                'client_size':len(clients),
                'daily_transaction_count':len(transaction),
                'registers':registers,
                'rate': product,
                'transaction':transactions,
                'countries':countries,
                'country_size':len(countries)
            }
            return render(request,'account/admin/dashboard.html', context)
        else:
            logout(request)
            context = {
                'message_authentication':'You are not allowed to access this page'
            }
            return render(request, 'authentication/registration/login.html',context)



@login_required
def account_profile(request):
    '''
    admin profile
    '''
    user = request.user
    if request.method == 'GET':
        if Account.objects.filter(user=user).exists():
            account = get_object_or_404(Account, user=user)
            return render(request, 'account/profile/profile.html',{'account':account})
        else:
            logout(request)
            context = {
                'message_authentication':'You are not allowed to access this page'
            }
            return render(request, 'authentication/registration/login.html',context)
    if request.method == 'POST':
        if request.POST['username']:
            user.username = request.POST['username']
        if request.POST['first_name']:
            user.first_name = request.POST['first_name']
        if request.POST['last_name']:
            user.last_name = request.POST['last_name']
        if request.POST['email']:
            user.email = request.POST['email']
        user.save()
        return redirect(account_profile)


@login_required
def account_profile_password(request):
    '''
    modify user's password
    '''
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        if request.method == 'POST':
            if request.POST['password'] and request.POST['password-new'] and request.POST['password-new-confirm'] is not None:
                verify = user.check_password(request.POST['password'])
                if verify == True and request.POST['password-new'] == request.POST['password-new-confirm']:
                    user.set_password(request.POST['password-new'])
                    logger.info('user change password')
                    return redirect(account_profile)
                else:
                    logger.info('wrong password provided')
                    return render(request, 'account/profile/profile.html',{'account':account,'message':'wrong password'})
    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)


@login_required
def rate_setup(request):
    '''
    display and add rates
    '''
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        if request.method == 'GET':
            logger.info('showing rate page')
            rates = Product.objects.filter(location__company=company, is_active=True)
            countries = Country.objects.filter(company=company)
            locations = Location.objects.filter(company=company)
            context = {
                'rates':rates,
                'company':company,
                'countries':countries,
                'locations':locations,
            }
            return render(request,'account/admin/rates.html', context)
        if request.method == 'POST':
            from_country = get_object_or_404(Country, id=request.POST['from_country'])
            to_country = get_object_or_404(Country, id=request.POST['to_country'])
            rate = request.POST['rate']
            locate = request.POST['location']
            location = get_object_or_404(Location, id=locate)
            # verify if rate exist
            verify_rate = Product.objects.filter(from_country=from_country, to_country=to_country,location=location).exists()
            if verify_rate == True:
                product = get_object_or_404(Product, from_country=from_country, to_country=to_country,location=location)
                product.price = rate
                product.is_active = True
                product.save()
            else:
                product = Product(from_country=from_country, to_country=to_country,location=location, price = rate)
                product.save()
            return redirect(rate_setup)
            
    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)


@login_required
def rate_delete(request, rate_id):
    '''
    change status
    '''
    user = request.user
    if request.method == 'GET':
        if Account.objects.filter(user=user).exists():
            product = get_object_or_404(Product, pk=rate_id)
            product.is_active= False
            product.save()
            return redirect(rate_setup)
        else:
            logout(request)
            context = {
                'message_authentication':'You are not allowed to access this page'
            }
            return render(request, 'authentication/registration/login.html',context)


@login_required
def account_employees(request):
    '''
    list of employees
    '''
    user = request.user
    if request.method == 'GET':
        if Account.objects.filter(user=user).exists():
            account = get_object_or_404(Account, user=user)
            company = get_object_or_404(Company, account=account)
            employees = Employee.objects.filter(company=company)
            context ={
                'employee_size':len(employees),
                'employee':employees,
                'company':company,
            }
            return render(request,'account/admin/employee/employee.html', context)
        else:
            logout(request)
            context = {
                'message_authentication':'You are not allowed to access this page'
            }
            return render(request, 'authentication/registration/login.html',context)


@login_required
def account_emp_transfer(request, employee_id):
    '''
    show all employee transaction
    '''
    user = request.user
    if request.method == 'GET':
        if Account.objects.filter(user=user).exists():
            account = get_object_or_404(Account, user=user)
            company = get_object_or_404(Company, account=account)
            employee =  get_object_or_404(Employee, id=employee_id, company=company)
            transactions = OrderDetail.objects.filter(order__employee=employee)
            context ={
                'employee':employee,
                'company':company,
                'transactions':transactions
            }
            return render(request,'account/admin/employee/employee_transfer.html', context)
        else:
            logout(request)
            context = {
                'message_authentication':'You are not allowed to access this page'
            }
            return render(request, 'authentication/registration/login.html',context)


@login_required
def account_transfer(request, detail_id):
    '''
    show all employee transaction
    '''
    user = request.user
    if request.method == 'GET':
        if Account.objects.filter(user=user).exists():
            account = get_object_or_404(Account, user=user)
            company = get_object_or_404(Company, account=account)
            transaction = get_object_or_404(OrderDetail, pk=detail_id) 
            payment = Payment.objects.filter(order=transaction.order).first()
            context ={
                'company':company,
                'order':transaction,
                'payment':payment,
                'status':Transaction_Status.objects.all()
            }
            return render(request,'account/admin/invoice/invoice.html', context)
        else:
            logout(request)
            context = {
                'message_authentication':'You are not allowed to access this page'
            }
            return render(request, 'authentication/registration/login.html',context)
    if request.method == 'POST':
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        status = get_object_or_404(Transaction_Status, pk=request.POST['method'])
        comment = request.POST['comment']
        detail = get_object_or_404(OrderDetail, pk=detail_id) 
        order = detail.order
        order.comment = comment
        order.status = status
        order.save()
        logger.info(order.status)
        payment = Payment.objects.filter(order=order).first()
        context ={
            'company':company,
            'order':detail,
            'payment':payment,
            'status':Transaction_Status.objects.all()
        }
        return render(request,'account/admin/invoice/invoice.html', context)



@login_required
def account_clients(request):
    '''
    list of employees
    '''
    user = request.user
    if request.method == 'GET':
        if Account.objects.filter(user=user).exists():
            account = get_object_or_404(Account, user=user)
            company = get_object_or_404(Company, account=account)
            clients = Client.objects.filter(company=company)
            context ={
                'client':clients,
                'company':company,
            }
            return render(request,'account/admin/client/client.html', context)
        else:
            logout(request)
            context = {
                'message_authentication':'You are not allowed to access this page'
            }
            return render(request, 'authentication/registration/login.html',context)

