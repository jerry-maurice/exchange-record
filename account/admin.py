from django.contrib import admin
from  account.models import Account, Account_status, Account_Plan, Account_transaction

# Register your models here.
admin.site.register(Account)
admin.site.register(Account_Plan)
admin.site.register(Account_status)
admin.site.register(Account_transaction)