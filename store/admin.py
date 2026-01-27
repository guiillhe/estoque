from django.contrib import admin

from .models import (
    Supplier,
    Buyer,
    Season,
    Drop,
    Product,
    Order,
    OrderItem,
    Delivery
)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'created_date']

class BuyerAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'created_date']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'supplier', 'status', 'created_date']
    inlines = [OrderItemInline]
    readonly_fields = ['created_date']

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Season)
admin.site.register(Drop)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(OrderItem)