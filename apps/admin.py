from django.contrib import admin

from apps.models import Category, Order, OrderItem, Product

# Register your models here.
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Product)
