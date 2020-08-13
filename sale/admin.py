from django.contrib import admin
from  sale.models import Order, OrderDetail, Transaction_Status, Product, Fee, Coupon, Payment_Method, Payment_Status, Payment

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Product)
admin.site.register(Transaction_Status)
admin.site.register(Fee)
admin.site.register(Coupon)
admin.site.register(Payment_Method)
admin.site.register(Payment_Status)
admin.site.register(Payment)