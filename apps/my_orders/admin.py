from django.contrib import admin
from .models import OrderStatus, PurchaseOrderStatus

# Админка для статуса заказа
@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'estimated_arrival', 'created_at')
    search_fields = ('order__order_id', 'order__from_city__name', 'order__to_city__name')
    list_filter = ('status', 'created_at', 'estimated_arrival')
    readonly_fields = ('order',)  # Поле только для чтения
    fieldsets = (
        (None, {
            'fields': ('order', 'status', 'estimated_arrival', 'created_at')
        }),
    )
    ordering = ('-created_at',)  # Сортировка по убыванию даты создания

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct

# Админка для статуса выкупа
@admin.register(PurchaseOrderStatus)
class PurchaseOrderStatusAdmin(admin.ModelAdmin):
    list_display = ('purchase_order', 'status', 'estimated_arrival', 'created_at')
    search_fields = ('purchase_order__purchase_order_id', 'purchase_order__from_city__name', 'purchase_order__to_city__name')
    list_filter = ('status', 'created_at', 'estimated_arrival')
    readonly_fields = ('purchase_order',)  # Поле только для чтения
    fieldsets = (
        (None, {
            'fields': ('purchase_order', 'status', 'estimated_arrival', 'created_at')
        }),
    )
    ordering = ('-created_at',)  # Сортировка по убыванию даты создания

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct
