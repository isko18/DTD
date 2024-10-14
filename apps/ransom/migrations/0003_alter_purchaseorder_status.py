# Generated by Django 5.0 on 2024-10-12 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ransom', '0002_alter_purchaseorder_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('order_processing', 'Обработка заказа'), ('assigning_courier', 'Назначаем курьера'), ('courier_on_way', 'Курьер в пути'), ('order_shipped', 'Отгрузка заказа'), ('order_received', 'Заказ получен'), ('order_completed', 'Завершен')], default='order_processing', max_length=20, verbose_name='Статус'),
        ),
    ]