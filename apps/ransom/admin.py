from django.contrib import admin
from .models import PurchaseOrder

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'from_city', 'to_city', 'product_name', 'product_category', 'price', 'quantity', 'status', 'created_at')
    readonly_fields = ('created_at', 'order_id')  
    search_fields = ('from_city__name', 'to_city__name', 'product_name', 'order_id', 'sender_name', 'receiver_name')  # Поиск по городам, товару и заказу
    list_filter = ('from_city', 'to_city', 'product_category', 'status', 'created_at')  # Фильтрация по городам, категории товара и статусу
    ordering = ('-created_at',) 
    list_editable = ('status',)  
    list_per_page = 20  


    actions = ['mark_as_shipped']

    def mark_as_shipped(self, request, queryset):
        """Отметить выбранные заказы как отгруженные."""
        queryset.update(status='order_shipped')
        self.message_user(request, "Выбранные заказы были отмечены как отгруженные.")

    mark_as_shipped.short_description = "Отметить выбранные заказы как отгруженные"