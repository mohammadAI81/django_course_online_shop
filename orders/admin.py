from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'order', 'quantity']
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'last_name', 'is_paid', 'datetime_created']
    inlines = [
        OrderItemInLine,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'quantity']

