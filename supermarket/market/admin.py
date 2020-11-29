from django.contrib import admin

from market.models import Product, Order, OrderRow, Customer
# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderRow)
admin.site.register(Customer)