# Generated by Django 5.0 on 2024-09-07 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PurchaseOrder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order_id",
                    models.CharField(
                        editable=False,
                        max_length=10,
                        unique=True,
                        verbose_name="ID заказа",
                    ),
                ),
                (
                    "from_address",
                    models.CharField(max_length=255, verbose_name="Адрес откуда"),
                ),
                (
                    "from_delivery_type",
                    models.CharField(
                        choices=[("door", "От двери"), ("pickup", "Самовывоз")],
                        max_length=50,
                        verbose_name="Тип доставки откуда",
                    ),
                ),
                (
                    "to_address",
                    models.CharField(max_length=255, verbose_name="Адрес куда"),
                ),
                (
                    "to_delivery_type",
                    models.CharField(
                        choices=[("door", "От двери"), ("pickup", "Самовывоз")],
                        max_length=50,
                        verbose_name="Тип доставки куда",
                    ),
                ),
                (
                    "sender_name",
                    models.CharField(max_length=100, verbose_name="Имя отправителя"),
                ),
                (
                    "sender_phone",
                    models.CharField(max_length=20, verbose_name="Телефон отправителя"),
                ),
                (
                    "receiver_name",
                    models.CharField(max_length=100, verbose_name="Имя получателя"),
                ),
                (
                    "receiver_phone",
                    models.CharField(max_length=20, verbose_name="Телефон получателя"),
                ),
                (
                    "product_name",
                    models.CharField(max_length=255, verbose_name="Название товара"),
                ),
                ("product_url", models.URLField(verbose_name="Ссылка на товар")),
                ("article", models.CharField(max_length=100, verbose_name="Артикул")),
                ("color", models.CharField(max_length=50, verbose_name="Цвет товара")),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Цена"
                    ),
                ),
                ("quantity", models.PositiveIntegerField(verbose_name="Количество")),
                ("comment", models.TextField(blank=True, verbose_name="Комментарий")),
                (
                    "pickup_service",
                    models.BooleanField(
                        default=False, verbose_name="Услуга вылова товара"
                    ),
                ),
                (
                    "keep_shoe_box",
                    models.BooleanField(
                        default=False, verbose_name="Сохранить коробку из под обуви"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "from_city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchase_orders_from_city",
                        to="orders.city",
                        verbose_name="Город откуда",
                    ),
                ),
                (
                    "from_label",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="purchase_orders_from_label",
                        to="orders.label",
                        verbose_name="Название лейбла",
                    ),
                ),
                (
                    "product_category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="purchase_orders",
                        to="orders.productcategory",
                        verbose_name="Категория товара",
                    ),
                ),
                (
                    "to_city",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchase_orders_to_city",
                        to="orders.city",
                        verbose_name="Город куда",
                    ),
                ),
            ],
            options={
                "verbose_name": "Выкуп заказа",
                "verbose_name_plural": "Выкупы заказов",
                "ordering": ["-created_at"],
            },
        ),
    ]