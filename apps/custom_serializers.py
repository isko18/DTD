from rest_framework import serializers

from django.utils import timezone


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        value = timezone.localtime(value)
        formatted_date = value.strftime('%d.%m.%Y %H:%M')
        return formatted_date


class CustomTimeField(serializers.TimeField):
    def to_representation(self, value):
        formatted_time = value.strftime('%H:%M')
        return formatted_time


class CustomDateField(serializers.DateField):
    def to_representation(self, value):
        formatted_time = value.strftime('%d.%m.%Y')
        return formatted_time


class CustomDecimalField(serializers.DecimalField):

    def to_internal_value(self, data):
        data = data.replace(',', '.')
        return super(CustomDecimalField, self).to_internal_value(data)

