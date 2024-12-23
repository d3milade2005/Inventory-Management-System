from django.contrib import admin
from .models import Product, InventoryTransaction, Order, OrderItem, StockAlert
# Register your models here.

admin.site.register(Product)
admin.site.register(InventoryTransaction)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(StockAlert)