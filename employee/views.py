from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from  employee.models import Employee, Schedule
from sale.models import OrderDetail, Order, Product
from register.models import RegisterAssigned, Register_Log
from account.models import Account
from company.models import Company

from account.views import account_emp_transfer


import logging
from datetime  import date

# get an instance of a logger
logger =  logging.getLogger(__name__)


@login_required
def dashboard(request):
    '''
    dashboard showing summary of transaction
    '''
    user = request.user
    employee = get_object_or_404(Employee, user=user)
    location = employee.location
    if request.method == 'GET':
        transaction = Order.objects.filter(employee=employee).order_by('-placement')[:10]
        product = Product.objects.filter(is_active=True, location=location).order_by('-modified')[:10]
        log = Register_Log.objects.filter(employee=employee).order_by('-modified')[:10]
        register_assigned = RegisterAssigned.objects.filter(date=date.today(),employee=employee)
        data = []
        label = []
        for r in register_assigned:
            data.append(r.register.balance)
            name = str(r.register.country.name)
            label.append(name)
        context = {
            'transaction':transaction,
            'rate':product,
            'data':data, 
            'label':label,
            'log':log,
        }
        return render(request, 'employee/dashboard/dashboard.html',context)


@login_required
def profile(request):
    '''
    show info about user 
    '''
    user = request.user
    employee = get_object_or_404(Employee, user=user)
    if request.method == 'GET':
        return render(request, 'employee/profile/profile.html',{'employee':employee})
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
        return redirect(profile)


@login_required
def profile_password(request):
    '''
    modify user's password
    '''
    user = request.user
    employee = get_object_or_404(Employee, user=user)
    if request.method == 'POST':
        if request.POST['password'] and request.POST['password-new'] and request.POST['password-new-confirm'] is not None:
            verify = user.check_password(request.POST['password'])
            if verify == True and request.POST['password-new'] == request.POST['password-new-confirm']:
                user.set_password(request.POST['password-new'])
                logger.info('user change password')
                return redirect(profile)
            else:
                logger.info('wrong password provided')
                return render(request, 'employee/profile/profile.html',{'employee':employee,'message':'wrong password'})


@login_required
def schedule(request):
    '''display employee schedule
    '''
    employee = get_object_or_404(Employee, user=request.user)
    company  = employee.company
    if request.method == 'GET':
        schedule = Schedule.objects.filter(employee=employee)
        context = {
            'schedule':schedule,
            'company':company,
        }
        return  render(request, 'employee/schedule/schedule.html',context)


@login_required
def add_schedule(request, emp_id):
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        employee = get_object_or_404(Employee, id=emp_id)
        schedule = Schedule.objects.filter(employee=employee)
        if request.method == 'GET':
            context = {
                'schedule':schedule,
                'company':company,
                'employee':employee,
            }
            return render(request, 'employee/schedule/addSchedule.html', context)
        if request.method == 'POST':
            weekday = request.POST['weekday']
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            task = request.POST['task']
            location = employee.location
            company = company
            verify_date = Schedule.objects.filter(weekday = request.POST['weekday'],employee=employee).exists()
            logger.info(verify_date)
            if verify_date == False:
                schedule = Schedule(employee=employee, weekday=weekday, start_time=start_time, end_time=end_time, task=task, location=location)
                schedule.save()
            else:
                schedule_date = Schedule.objects.get(employee=employee)
                schedule_date.start_time = start_time
                schedule_date.end_time = end_time
                schedule_date.task = task
                schedule_date.location = location
                schedule_date.save()
            return redirect(account_emp_transfer, emp_id)
    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)


@login_required
def delete_schedule(request, emp_id, schedule_id):
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        employee = get_object_or_404(Employee, id=emp_id)
        schedule = Schedule.objects.filter(employee=employee, id=schedule_id)
        if request.method == 'GET':
            schedule.delete()
            return redirect(add_schedule, emp_id)
    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)
        


def handler404(request, exception):
    return render(request, 'error_pages/error_404.html', {})


def handler505(request):
    return render(request, 'error_pages/error_505.html', {})