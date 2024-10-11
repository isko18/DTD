# Generated by Django 5.0 on 2024-10-11 19:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Категория товара')),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товара',
            },
        ),
        migrations.CreateModel(
            name='SubCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Подгород')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcities', to='orders.city', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Подгород',
                'verbose_name_plural': 'Подгорода',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('order_processing', 'Обработка заказа'), ('assigning_courier', 'Назначаем курьера'), ('courier_on_way', 'Курьер в пути'), ('order_shipped', 'Отгрузка заказа'), ('order_received', 'Заказ получен')], default='order_processing', max_length=20, verbose_name='Статус')),
                ('estimated_arrival', models.DateTimeField(blank=True, null=True, verbose_name='Примерное время прибытия')),
                ('order_id', models.CharField(editable=False, max_length=10, unique=True, verbose_name='ID заказа')),
                ('from_address', models.CharField(max_length=255, verbose_name='Адрес откуда')),
                ('from_delivery_type', models.CharField(choices=[('door', 'От двери'), ('pickup', 'Самовывоз')], max_length=50, verbose_name='Тип доставки откуда')),
                ('to_address', models.CharField(max_length=255, verbose_name='Адрес куда')),
                ('to_delivery_type', models.CharField(choices=[('door', 'От двери'), ('pickup', 'Самовывоз')], max_length=50, verbose_name='Тип доставки куда')),
                ('delivery_cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость доставки')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('from_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_from_city', to='orders.city', verbose_name='Город откуда')),
                ('to_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_to_city', to='orders.city', verbose_name='Город куда')),
                ('product_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='orders.productcategory', verbose_name='Категория товара')),
                ('from_subcity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_from_subcity', to='orders.subcity', verbose_name='Подгород откуда')),
                ('to_subcity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_to_subcity', to='orders.subcity', verbose_name='Подгород куда')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-created_at'],
            },
        ),
    ]
