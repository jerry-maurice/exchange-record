from django.contrib import admin
from company.models import Company, Location


# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'about', 'account')
    list_filter = ('name', 'about', 'account',)
    search_fields = ('name',)
    ordering =  ('name',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('phone', 'fax','house_number','address', 'city','zipcode', 'state','country','company')