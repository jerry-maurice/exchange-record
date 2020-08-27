from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from overview.views import index

from account.models import Account
from account.views import account_dashboard

from employee.views import dashboard

from employee.models import Employee, Schedule

import logging
from datetime import date,  datetime
from django.utils import timezone

# get an instance of a logger
logger =  logging.getLogger(__name__)

# Create your views here.
def authentication(request):
    '''
    login verification
    '''
    if request.method == 'GET':
        return render(request, 'authentication/registration/login.html')
    if  request.method == 'POST':
        username = request.POST['login-username']
        password = request.POST['login-password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                verify_account = Account.objects.filter(user=user).exists()
                if verify_account == True:
                    # redirect to  account holder view
                    return redirect(account_dashboard)
                else:
                    # redirect to employee view
                    emp = get_object_or_404(Employee, user=user)
                    day = timezone.now().weekday()
                    if Schedule.objects.filter(employee=emp, weekday=(day+1)).exists():
                        schedule = get_object_or_404(Schedule, employee=emp, weekday=day+1)
                        # logger.info(timezone.now().time())
                        # logger.info(datetime.now().time())
                        start_time = schedule.start_time
                        end_time  = schedule.end_time
                        if checkTime(start_time, end_time) == True:
                            return  redirect(dashboard)
                        else:
                            logout(request)
                            context = {
                                'message_authentication':'You shift does not start yet'
                            }
                            return render(request, 'authentication/registration/login.html',context)
                    else:
                        logout(request)
                        context = {
                            'message_authentication':'Please contact your manager. You are not schedule to work'
                        }
                        return render(request, 'authentication/registration/login.html',context)
        else:
            context = {
                'message_authentication':'Please try again. User not found'
            }
            return render(request, 'authentication/registration/login.html',context)



def locked(request):
    '''
    locked account
    '''
    if request.method == 'GET':
        user = request.user
        context = {
            'email':user.email,
            'username':user.username
        }
        return render(request, 'authentication/registration/locked.html',context)
    if request.method == 'POST':
        username = request.POST['lock-username']
        password = request.POST['lock-password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                verify_account = Account.objects.filter(user=user).exists()
                if verify_account == True:
                    # redirect to  account holder view
                    return redirect(account_dashboard)
                else:
                    # redirect to employee view
                    emp = get_object_or_404(Employee, user=user)
                    if Schedule.objects.filter(employee=emp).exists():
                        day = timezone.now().weekday()
                        schedule = Schedule.objects.filter(employee=emp, weekday=day)
                        start_time = schedule.start_time
                        end_time  = schedule.end_time
                        if checkTime(start_time, end_time) == True:
                            return  redirect(dashboard)
                        else:
                            logout(request)
                            context = {
                                'message_authentication':'You shift does not start yet'
                            }
                            return render(request, 'authentication/registration/login.html',context)
                    else:
                        logout(request)
                        context = {
                            'message_authentication':'Please contact your manager. You are not schedule to work'
                        }
                        return render(request, 'authentication/registration/login.html',context)

        else:
            logout(request)
            context = {
                'message_authentication':'Please try again. User not found'
            }
            return render(request, 'authentication/registration/login.html',context)



def loging_out(request):
    '''
    logout  
    '''
    logout(request)
    return redirect(index)


def checkTime(start_time, end_time):
    timenow = datetime.now().time()
    if timenow >= start_time and timenow <= end_time:
        return True
    else:
        return False
     
