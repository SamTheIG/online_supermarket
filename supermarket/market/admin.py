from django.contrib import admin

from market.models import *

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderRow)
