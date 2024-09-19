import re


def normalize_phone_number(phone_number):
    # Удаляем все нецифровые символы
    digits = re.sub(r'\D', '', phone_number)
    if digits.startswith('0'):
        return "+996" + digits[1:]
    if digits.startswith('996'):
        return "+" + digits
    else:
        return "+996" + digits
