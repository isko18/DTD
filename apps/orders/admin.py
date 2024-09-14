from django.contrib import admin
from .models import City, SubCity, ProductCategory, Order

class SubCityInline(admin.TabularInline):
    model = SubCity
    extra = 1
    verbose_name = "Подгород"
    verbose_name_plural = "Подгорода"

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    inlines = [SubCityInline]
    ordering = ('name',)  # Сортировка городов по имени

@admin.register(SubCity)
class SubCityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    search_fields = ('name', 'city__name')  # Поиск по названию города и подгорода
    list_filter = ('city',)  # Фильтр по городу
    ordering = ('name',)  # Сортировка по названию подгорода

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)  # Сортировка по названию категории

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_id', 'from_city', 'from_subcity', 'to_city', 'to_subcity', 'product_category', 'delivery_cost', 'status', 'created_at')
    search_fields = ('from_city__name', 'to_city__name', 'from_subcity__name', 'to_subcity__name', 'product_category__name', 'order_id')  # Добавлен поиск по подгородам и ID заказа
    list_filter = ('from_city', 'to_city', 'product_category', 'status', 'created_at')  # Фильтр по статусу заказа
    ordering = ('-created_at',)  # Заказы отсортированы по дате создания
    readonly_fields = ('created_at', 'order_id')  # Добавлено поле для чтения order_id
    list_editable = ('status',)  # Возможность изменять статус заказа из списка заказов

    # Дополнительные действия для удобства в админке
    actions = ['mark_as_shipped']

    def mark_as_shipped(self, request, queryset):
        """Отметить выбранные заказы как отгруженные."""
        queryset.update(status='order_shipped')
        self.message_user(request, "Выбранные заказы были отмечены как отгруженные.")

    mark_as_shipped.short_description = "Отметить выбранные заказы как отгруженные"
