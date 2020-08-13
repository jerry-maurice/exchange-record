from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from  company.models import Company, Location
from country.models import Country
from client.models import Client
from employee.models import Employee
from  decimal import Decimal
import math

# Create your models here.
class Fee(models.Model):
    '''
    transfer fee
    '''
    amount =  models.FloatField(null=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='fee_location' )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.amount}' 


class Coupon(models.Model):
    '''
    discount code
    '''
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='coupon_company')

    @property
    def discount_percentage(self):
        return self.discount /Decimal(100)

    def __str__(self):
        return self.code 


class Product(models.Model):
    '''
    rate of change for each country
    '''
    from_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_rate_from')
    to_country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_rate_to')
    price = models.FloatField(null=False)
    modified = models.DateField(auto_now=True)
    added = models.DateField(auto_now_add=True)
    location = models.ForeignKey(Location, on_delete = models.CASCADE,  related_name='rate_location')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.from_country.name} to {self.to_country.name} - {self.price}"


class  Payment_Method(models.Model):
    '''
    list of method of payment
    '''
    name = models.CharField(null=False, max_length=250)

    def __str__(self):
        return self.name 


class Payment_Status(models.Model):
    '''
    list of status of payment
    '''
    name = models.CharField(null=False, max_length=250)

    class Meta:
        verbose_name = 'Payment_status'
        verbose_name_plural = 'Payment_status'

    def __str__(self):
        return self.name 


class Transaction_Status(models.Model):
    '''
    list of status of payment
    '''
    name = models.CharField(null=False, max_length=250)

    def __str__(self):
        return self.name 


class Order(models.Model):
    '''
    customer order
    '''
    placement = models.DateTimeField(auto_now_add=True)
    fulfillment = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Client, on_delete = models.CASCADE,  related_name='client_order')
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE,  related_name='employee_order')
    location = models.ForeignKey(Location, on_delete = models.CASCADE,  related_name='order_location')
    status = models.ForeignKey(Transaction_Status, on_delete = models.CASCADE,  related_name='transaction_status')
    comment = models.TextField()

    class Meta:
        ordering = ('-placement',)

    def __str__(self):
        return f'{self.customer.first_name}. {self.employee.user.first_name}. {self.status.name}. {self.comment}'


class OrderDetail(models.Model):
    '''
    detail about order
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
    quantity = models.FloatField(null=False)
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name='order_fee', blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete = models.CASCADE, related_name='order_coupon', blank=True, null=True)
    order = models.ForeignKey(Order, on_delete= models.CASCADE, related_name='order_detail', null=True)

    @property
    def total_price(self):
        return round(self.product.price * self.quantity,2)

    @property
    def total_discount(self):
        if self.coupon is not None:
            return self.total_price() * (self.coupon.discount /Decimal(100))
        return self.product.price * self.quantity

    @property
    def grand_total(self):
        return self.total_discount + self.fee.amount

    @property
    def fee_amount(self):
        return math.floor(self.quantity * (self.fee.amount /(100)))

    @property
    def exchange_total_due(self):
        return self.quantity + (self.fee_amount)

    def __str__(self):
        return f'{self.product.price}. {self.quantity}. {self.fee}'


class Payment(models.Model):
    '''
    record of payment made  by customer
    '''
    method = models.ForeignKey(Payment_Method, on_delete = models.CASCADE,  related_name='method_payment')
    status = models.ForeignKey(Payment_Status, on_delete = models.CASCADE,  related_name='status_payment')
    amount = models.FloatField()
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
    customer = models.ForeignKey(Client, on_delete = models.CASCADE,  related_name='client_payment')
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name='payment_order')
    comment = models.TextField()


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.amount}'
