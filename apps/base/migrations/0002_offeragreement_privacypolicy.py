# Generated by Django 5.0 on 2024-10-21 13:12

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferAgreement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptions', ckeditor.fields.RichTextField(verbose_name='ДОГОВОР ОФЕРТЫ')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': 'ДОГОВОР ОФЕРТЫ',
            },
        ),
        migrations.CreateModel(
            name='PrivacyPolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descriptions', ckeditor.fields.RichTextField(verbose_name='ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': 'ПОЛИТИКА КОНФИДЕНЦИАЛЬНОСТИ',
            },
        ),
    ]
