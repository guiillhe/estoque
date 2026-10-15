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
    list_display = ['user', 'name', 'enterprise', 'address', 'created_date']
    list_filter = ['enterprise']

class BuyerAdmin(admin.ModelAdmin):
    list_display = ['sub_id', 'name', 'enterprise', 'user', 'setor', 'created_date']
    list_filter = ['enterprise', 'setor']
    search_fields = ['sub_id', 'name', 'cpf', 'user__username', 'user__email']

class SeasonAdmin(admin.ModelAdmin):
    list_display = ['name', 'enterprise', 'created_date']
    list_filter = ['enterprise']

class DropAdmin(admin.ModelAdmin):
    list_display = ['name', 'enterprise', 'created_date']
    list_filter = ['enterprise']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'enterprise', 'quantity', 'unit_of_measurement', 'is_active']
    list_filter = ['enterprise', 'is_active']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'enterprise', 'buyer', 'supplier', 'status', 'created_date']
    list_filter = ['enterprise', 'status']
    inlines = [OrderItemInline]
    readonly_fields = ['created_date']

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'enterprise', 'order', 'courier_name', 'created_date']
    list_filter = ['enterprise']

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Drop, DropAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(OrderItem)