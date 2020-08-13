from django.db import models
from phone_field import PhoneField
from account.models import Account

# Create your models here.
class Company(models.Model):
    '''detail about the company'''
    name = models.CharField(max_length=250, null=False)
    about = models.TextField(null=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='company_account')

    class Meta:
        ordering = ('name',)
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.name


class Location(models.Model):
    '''Base model for the locations of a company'''
    phone = PhoneField(blank=False, help_text='company phone number' )
    fax = PhoneField(blank=False, help_text='company fax number' )
    house_number = models.CharField(max_length=50)
    address = models.CharField(max_length=250, null=False)
    city = models.CharField(max_length=250, null=False)
    zipcode = models.CharField(max_length=10, null=True)
    state = models.CharField(max_length=250, null=False)
    country = models.CharField(null=False, max_length=250, default='Haiti')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='location_company')

    def __str__(self):
        return self.house_number+' '+ self.address+' '+self.city+' '+self.country