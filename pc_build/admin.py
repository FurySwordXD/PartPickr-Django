from django.contrib import admin
from .models import Part, Cart, Order, Shopping_Cart
# Register your models here.
admin.site.register(Part)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Shopping_Cart)