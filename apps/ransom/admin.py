from django.contrib import admin
from .models import PurchaseOrder

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id' ,'product_name', 'receiver_name', 'from_city', 'to_city', 'price', 'created_at')
    search_fields = ('product_name', 'receiver_name', 'from_city__name', 'to_city__name')
    list_filter = ('from_city', 'to_city', 'product_category', 'created_at')
    ordering = ('-created_at',)
