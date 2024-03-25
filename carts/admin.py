from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')
    search_fields = ('cart_id',)  # Add fields you want to search by
    list_filter = ('date_added',)  # Add fields you want to filter by


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.site_header = "DiMiPi Demo Shop Administration"
admin.site.site_title = "DiMiPi Admin Portal"
admin.site.index_title = "Welcome to My Shop Admin"
