from django.contrib import admin
from employee.models import Employee, Employee_status, Schedule

# Register your models here.
admin.site.register(Employee)
admin.site.register(Employee_status)
admin.site.register(Schedule)