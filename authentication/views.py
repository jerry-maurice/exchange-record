from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from overview.views import index

from account.models import Account
from account.views import account_dashboard

from employee.views import dashboard

import logging

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
                    logger.info('account holder verified')
                else:
                    # redirect to employee view
                    logger.info('account not found')
                    return  redirect(dashboard)
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
                    logger.info('account holder verified')
                else:
                    # redirect to employee view
                    logger.info('account not found')
                    return  redirect(dashboard)
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

