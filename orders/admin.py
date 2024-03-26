from django.contrib import admin
from .models import Payment, Order, OrderProduct


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number']

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)
