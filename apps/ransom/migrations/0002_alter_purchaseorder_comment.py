# Generated by Django 5.0 on 2024-10-11 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ransom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
    ]
