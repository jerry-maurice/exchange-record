from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from company.models import Company, Location
from fund.models import Fund, FundTransaction
from country.models import Country
from account.models import Account

import logging

# get an instance of a logger
logger =  logging.getLogger(__name__)

# Create your views here.
def fund_overview(request):
    '''
    display the amount of money available for each currency
    '''
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        if request.method == 'GET':
            funds = Fund.objects.filter(company=company)
            countries = Country.objects.filter(company=company)
            context = {
                'fund':funds,
                'company':company,
                'countries':countries,
            }
            return render(request,'fund/overview/overview.html',context)
        if request.method == 'POST':
            country = get_object_or_404(Country, id=request.POST['country']) 
            if Fund.objects.filter(company=company, country=country).exists():
                return redirect(fund_overview)
            else:
                fund = Fund(country=country, company=company)
                fund.save()
                return redirect(fund_overview)
    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)


def log_display(request, fund_id):
    '''
    return the list of transactions
    '''
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        if request.method == 'GET':
            fund = get_object_or_404(Fund, id=fund_id)
            logs = FundTransaction.objects.filter(fund=fund)
            context = {
                'logs':logs,
                'company':company,
            }
            return render(request,'fund/log/log.html',context)
    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)


def fund_deposit(request, fund_id):
    '''
    return the list of transactions
    '''
    user = request.user
    if Account.objects.filter(user=user).exists():
        account = get_object_or_404(Account, user=user)
        company = get_object_or_404(Company, account=account)
        fund = get_object_or_404(Fund, id=fund_id)
        if request.method == 'GET':
            context = {
                'fund':fund,
                'company':company,
            }
            return render(request,'fund/operation/deposit.html',context)
        if request.method == 'POST':
            deposit_amount = request.POST['amount']
            source = request.POST['source']
            comment = request.POST['comment']
            previous_amount = fund.funds
            actual_balance = float(previous_amount) + float(deposit_amount)
            fund.funds = actual_balance
            fund.save()
            transaction = FundTransaction(deposited=deposit_amount, previous_balance=previous_amount, 
                        actual_balance=actual_balance, source=source, fund=fund, comment=comment)
            transaction.save()
            return redirect(fund_overview)
    else:
        logout(request)
        context = {
            'message_authentication':'You are not allowed to access this page'
        }
        return render(request, 'authentication/registration/login.html',context)

    
