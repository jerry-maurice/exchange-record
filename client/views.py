from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from client.models import  Client
from employee.models import Employee

import logging

# get an instance of a logger
logger =  logging.getLogger(__name__)

# Create your views here.
@login_required
def client(request):
    '''
    list of client
    '''
    user = request.user
    employee = get_object_or_404(Employee, user=user)
    company = employee.company
    clients = Client.objects.filter(company=company)
    if request.method == 'GET':
        context = {
            'clients':clients,
            'company':company,
        }
        return render(request,'client/list/clients.html', context)


@login_required
def add_client(request):
    '''
    add client
    '''
    user = request.user
    employee = get_object_or_404(Employee, user=user)
    company = employee.company
    if request.method ==  'GET':
        context = {
            'company':company,
        }
        return render(request,'client/add/client_add.html',context)
    if request.method == 'POST':
        nif = request.POST['identification']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        gender = request.POST['gender']
        dob = request.POST['dob']
        phone = request.POST['phone']
        data = Client(identification=nif, first_name=first_name,  last_name=last_name, 
                        email=email, gender=gender, dob=dob, phone=phone,company=company)
        data.save()
        return redirect(client)

