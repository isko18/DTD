from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderItem

class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1  # Количество пустых форм для добавления новых товаров в заказ
    readonly_fields = ('price',)  # Поля только для чтения, если необходимо

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'from_city', 'to_city', 'status', 'created_at')  # Убраны поля товара, так как они относятся к PurchaseOrderItem
    readonly_fields = ('created_at', 'order_id')  
    search_fields = ('from_city__name', 'to_city__name', 'order_id', 'sender_name', 'receiver_name')  # Убраны поля для поиска по товару
    list_filter = ('from_city', 'to_city', 'status', 'created_at')  # Фильтрация по городам и статусу
    ordering = ('-created_at',) 
    list_editable = ('status',)  
    list_per_page = 20

    inlines = [PurchaseOrderItemInline]  # Добавляем инлайн для товаров в заказе

    actions = ['mark_as_shipped']

    def mark_as_shipped(self, request, queryset):
        """Отметить выбранные заказы как отгруженные."""
        queryset.update(status='order_shipped')
        self.message_user(request, "Выбранные заказы были отмечены как отгруженные.")

    mark_as_shipped.short_description = "Отметить выбранные заказы как отгруженные"
