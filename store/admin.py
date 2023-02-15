from django.contrib import admin
from .models import Product,Order,Cart,Persondetails


# Register your models here.
admin.site.register(Product)
admin.site.register(Persondetails)
admin.site.register(Order)
admin.site.register(Cart)