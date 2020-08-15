from django.db import models
from company.models import Location, Company
from employee.models import Employee
from country.models import Country

# Create your models here.
class Register_Status(models.Model):
    '''
    list of status
    '''
    name = models.CharField(null=False, max_length=250)
        
    def __str__(self):
        return self.name


class Register(models.Model):
    '''
    cash register
    '''
    identification = models.CharField(null=False, max_length=500)
    balance = models.FloatField(null=False)
    min_balance = models.FloatField(null=False)
    max_balance = models.FloatField(null=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location_register')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_register')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_register')
    created = models.DateField(auto_now=True)
    status = models.ForeignKey(Register_Status, on_delete=models.CASCADE, related_name='status_register')

    class Meta:
        ordering = ('identification',)
        
    def __str__(self):
        return f'{self.identification}. {self.balance}'


class Register_Log(models.Model):
    '''
    all transactions made are recorded
    '''
    deposited = models.FloatField(null=False, default=0.0)
    withdrew = models.FloatField(null=False, default=0.0)
    previous_balance = models.FloatField(null=False, default=0.0)
    actual_balance = models.FloatField(null=False, default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    register = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='log_register')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_register')

    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return f'{self.created}. {self.previous_balance}. {self.actual_balance}'


class RegisterAssigned(models.Model):
    '''
    assigned register to each employee
    '''
    date =  models.DateField(null=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_register_assigned')
    register = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='register_assigned_emp')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_assigned_emp', null=True)

    def __str__(self):
        return f'{self.employee}. -> {self.register.identification}. {self.register.balance}'