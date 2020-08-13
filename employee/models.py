from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from company.models import Location, Company
from datetime import datetime

# Create your models here.
class Employee_status(models.Model):
    '''
    list of status
    '''
    name = models.CharField(null=False, max_length=250)

    class Meta:
        verbose_name = 'Employee_status'
        verbose_name_plural = 'Employee_status'
        
    def __str__(self):
        return self.name


class Employee(models.Model):
    '''Base model for an employee'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    picture = models.URLField(null=True)
    title = models.CharField(max_length=250, null=True)
    gender = models.CharField(max_length=50, null=False)
    date_of_birth = models.DateField(null=False)
    hire_date = models.DateField(null=True)
    phone = PhoneField(blank=False, help_text='employee phone number' )
    emergency_contact = models.CharField(max_length=20, null=False)
    status = models.ForeignKey(Employee_status, on_delete=models.CASCADE, related_name='employee_status')
    # address detail
    house_number = models.CharField(max_length=50)
    address = models.CharField(max_length=250, null=False)
    city = models.CharField(max_length=250, null=False)
    zipcode = models.CharField(max_length=10, null=True)
    state = models.CharField(max_length=250, null=False)
    # record fields
    updated_on = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    # company
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='employee_location')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employee_company', blank=True, null=True)

    @property
    def age(self):
        '''
        property to calculate the age of an employee
        '''
        if self.dob:
            return int((datetime.now().date() - self.dob).days / 365.25)
        else:
            return None


    def __str__(self):
        return self.user.first_name+' '+self.user.last_name



class Schedule(models.Model):
    weekday = models.IntegerField(null=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    date = models.DateField(null=True)
    task = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_schedule', blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='schedule_location')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='schedule_company', blank=True, null=True)

    class Meta:
            ordering = ('weekday',)

    @property
    def day_of_week(self):
        name = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
        return name[self.weekday]
    
        
    def __str__(self):
        return "{}".format(self.date)


