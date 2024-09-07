from django.contrib import admin
from .models import City, SubCity, Label, ProductCategory, Order

# Инлайн для подгородов
class SubCityInline(admin.TabularInline):
    model = SubCity
    extra = 1  # Количество пустых строк для добавления подгородов
    verbose_name = "Подгород"
    verbose_name_plural = "Подгорода"

# Регистрация модели City с инлайнами для подгородов
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    inlines = [SubCityInline]  # Добавляем подгорода как инлайн

# Регистрация модели SubCity
@admin.register(SubCity)
class SubCityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city')
    search_fields = ('name', 'city__name')  # Поиск по названию подгорода и города
    list_filter = ('city',)  # Фильтр по городу

# Регистрация модели Label
@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Регистрация модели ProductCategory
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Регистрация модели Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','order_id', 'from_city', 'to_city', 'product_category', 'delivery_cost', 'created_at')
    search_fields = ('from_city__name', 'to_city__name', 'product_category__name')
    list_filter = ('from_city', 'to_city', 'product_category', 'created_at')
    ordering = ('-created_at',)  # Сортировка по дате создания
    readonly_fields = ('created_at',)  # Поле только для чтения
