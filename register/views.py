from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from  employee.models import Employee
from register.models import  Register, Register_Status, RegisterAssigned


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