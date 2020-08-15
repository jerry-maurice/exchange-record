from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from client.models import Client
from employee.models import Employee
from  sale.models import Order, OrderDetail, Transaction_Status, Product, Fee, Payment_Method, Payment, Payment_Status
from  country.models import Country
from register.models import RegisterAssigned, Register_Log

from client.views import add_client

import logging
from datetime import date,  datetime

# get an instance of a logger
logger =  logging.getLogger(__name__)

# Create your views here.
@login_required
def search_client(request):
    '''
    search client to start the application
    '''
    user = request.user
    employee = get_object_or_404(Employee, user=user)
    company = employee.company
    location = employee.location
    if request.method == 'GET':
        return render(request, 'sale/app/search_client.html')
    if request.method == 'POST':
        phone = request.POST['phone']
        client = Client.objects.filter(phone=phone, company=company).first()
        if client is None:
            return redirect(add_client)
        else:
            status = Transaction_Status.objects.get(name="PENDING..")
            order = Order(customer=client, employee=employee, location=location, status=status)
            order.save()
            return redirect(order_detail, order_id=order.id)


@login_required
def order_detail(request, order_id):
    '''
    part 2 of the exchange app
    '''
    employee = get_object_or_404(Employee, user=request.user)
    company = employee.company
    location = employee.location
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'GET':
        from_country = Country.objects.filter(company=company)
        to_country = Country.objects.filter(company=company)
        context = {
            'from_country':from_country,
            'to_country':to_country,
            'order_id':order_id
        }
        return render(request, 'sale/app/select_product.html',context)
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=order_id)
        from_country = get_object_or_404(Country, pk=request.POST['from_country'])
        to_country = get_object_or_404(Country, pk=request.POST['to_country'])
        logger.info(to_country)
        logger.info(from_country)
        product = get_object_or_404(Product, from_country=from_country, to_country=to_country, location=location)
        fee = Fee.objects.all().first()
        detail = OrderDetail(product=product, quantity=request.POST['selling_price'], order=order,fee=fee)
        detail.save()
        return redirect(submit_order,order_id=order.id, detail_id=detail.id)



@login_required
def submit_order(request, order_id, detail_id):
    '''
    part 3 of the exchange app
    '''
    employee = get_object_or_404(Employee, user=request.user)
    company = employee.company
    location = employee.location
    detail = get_object_or_404(OrderDetail, pk=detail_id)
    payment_method = Payment_Method.objects.all()
    # search for assigned registers
    register_assigned = RegisterAssigned.objects.filter(date=date.today(),employee=employee)
    registers = []
    from_register = None
    to_register = None
    for r in register_assigned:
        registers.append(r.register)
        if r.register.country.name == detail.product.from_country.name:
            from_register  = r.register
            logger.info(from_register)
        if r.register.country.name == detail.product.to_country.name:
            to_register =  r.register
            logger.info(to_register)

    if request.method == 'GET':
        context= {
            'order':detail,
            'company':company,
            'employee':employee,
            'location':location,
            'customer':detail.order.customer,
            'payment_method':payment_method,
        }
        return render(request, 'sale/app/submit_order.html',context)
    if request.method == 'POST':
        if register_assigned.exists() == False:
            # if no register assigned return error message
            context = {
                'message':'You were not  assigned any cash registers. Please contact your manager'
            }
            return render(request, 'sale/message/message.html',context)
        method = get_object_or_404(Payment_Method, id=request.POST['method'])
        status = get_object_or_404(Payment_Status, name="SUCCESSFUL")
        payment = Payment(method=method, status=status,amount=request.POST['amount'],customer=detail.order.customer,order=detail.order)
        payment.save()
        o_status = Transaction_Status.objects.get(name="COMPLETED")
        order = detail.order
        if detail.total_price > to_register.balance:
            c_status = Transaction_Status.objects.get(name="CANCELLED")
            order.status = c_status
            order.comment = 'Cash register \' balance is low. Order has been cancelled. Please add  more fund to this cash register'
            order.save()
            context = {
                'message':'Cash register \' balance is low. Order has been cancelled. Please add  more fund to this cash register'
            }
            return render(request, 'sale/message/message.html',context)
        order.status = o_status
        order.fulfillment = datetime.now()
        order.save()
        change_due = float(detail.exchange_total_due) -  float(payment.amount)
        '''
        updating register and log
        since two registers are involved, there will be two  log input
        '''
        #  log 1 and register 1
        log1_previous_balance = float(from_register.balance)
        log1_withdrew = 0.0
        log1_deposited = float(detail.exchange_total_due)
        from_register.balance = log1_previous_balance + log1_deposited
        from_register.save()
        log1 = Register_Log(actual_balance = from_register.balance, withdrew=log1_withdrew, previous_balance=log1_previous_balance, deposited = log1_deposited, register=from_register,  employee=employee)
        log1.save()

        # log 2 and register 2
        log2_previous_balance = float(to_register.balance) 
        log2_deposited = 0.0
        log2_withdrew = float(detail.total_price)
        to_register.balance = log2_previous_balance - log2_withdrew
        to_register.save()
        log2 = Register_Log(actual_balance = to_register.balance, withdrew=log2_withdrew, previous_balance=log2_previous_balance, deposited = log2_deposited, register=to_register,  employee=employee)
        log2.save()

        context= {
            'order':detail,
            'company':company,
            'employee':employee,
            'location':location,
            'customer':detail.order.customer,
            'payment':payment,
            'change':change_due,
        }
        return render(request, 'sale/invoice/invoice.html',context)


@login_required
def sale_summary(request):
    '''
    transaction summary
    '''
    employee = get_object_or_404(Employee, user=request.user)
    company = employee.company
    if request.method == 'GET':
        summary = OrderDetail.objects.filter(order__employee=employee)
        context = {
            'summary':summary,
            'company':company
        }
        return render(request,  'sale/invoice/sales.html',{'summary':summary})

