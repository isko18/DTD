import os
import uuid
import re


def custom_upload_path(instance, filename):
    """Генерация имен для файлов для upload_to в ImageField"""
    ext = os.path.splitext(filename)[1]
    unique_filename = f"{uuid.uuid4()}{ext}"
    return f"{instance.__class__.__name__}/{unique_filename}"


def validate_kyrgyz_phone_number(value):
    kyrgyz_number_pattern = r'^\+996\d{9}$'
    if not re.match(kyrgyz_number_pattern, value):
        return False
    return True
