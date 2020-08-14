from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from datetime import timedelta, date
from plan.models  import Plan

# Create your models here.
class Account_status(models.Model):
    '''
    list of status
    '''
    name = models.CharField(null=False, max_length=250)

    class Meta:
        verbose_name = 'Account_status'
        verbose_name_plural = 'Account_status'
        
    def __str__(self):
        return self.name


class Account(models.Model):
    '''
    Account holder detail info
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneField(blank=False, help_text='Account holder phone number' )
    status = models.ForeignKey(Account_status, on_delete=models.CASCADE, related_name='account_status')
        
    def __str__(self):
        return self.user.username


class Account_Plan(models.Model):
    '''
    Chosen plan
    '''
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='account_plan')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_holder')
    started = models.DateTimeField(auto_now_add=True)
    trial = models.BooleanField(default=False)

    @property
    def renew_date(self):
        return self.started +  timedelta(days=30)
        
    def __str__(self):
        return self.plan.name +' - '+ self.account.user.email


class Account_transaction(models.Model):
    '''
    list of bills and payments
    '''
    bill_created = models.DateField(auto_now_add=True)
    bill_due = models.DateField(null=False)
    bill_modified = models.DateField(auto_now=True)
    amount_due = models.FloatField(null=False)
    amount_due_currency = models.CharField(null=True, max_length=250)
    amount_received = models.FloatField(null=False, default=0.00)
    amount_received_currency = models.CharField(null=True, max_length=250)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_transaction_holder')
    account_plan = models.ForeignKey(Account_Plan, on_delete=models.CASCADE, related_name='account_transaction_plan')

    class Meta:
        ordering = ('-bill_created',)
        
    def __str__(self):
        return "{}".format(self.bill_due)