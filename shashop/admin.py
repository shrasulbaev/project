from django.contrib import admin
from .models import Category, Order, OrderItem, Product


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    pass


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    pass


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class AdminOrderItem(admin.ModelAdmin):
    pass
