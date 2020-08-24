from django.contrib import admin
from fund.models import Fund, FundTransaction

# Register your models here.
admin.site.register(Fund)
admin.site.register(FundTransaction)