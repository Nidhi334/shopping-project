from django.contrib import admin
from .models import *

admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Coupon)

# Register your models here.
