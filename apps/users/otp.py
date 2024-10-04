import requests
import xmltodict
from datetime import datetime
from django.conf import settings
from dicttoxml import dicttoxml

def send_nikita_sms(user, phone_number=None):
    if not settings.NIKITA_URL:
        return False
    
    # Генерация уникального идентификатора для сообщения
    id_string = '%s%d' % (user.id, datetime.now().timestamp())
    
    # Если номер телефона не передан, используем номер пользователя
    if not phone_number:
        phone_number = user.phone_number
    
    # Проверка, если номер телефона является тестовым
    if phone_number == "+996111111":
        # Включение тестового режима и установка кода 123456
        settings.NIKITA_TEST = "1"
        user.verification_code = "123456"
    else:
        # Генерация и сохранение кода подтверждения, если не тестовый режим
        user.generate_and_save_verification_code()
    
    # Формируем сообщение
    message = f"Ваш код верификации: {user.verification_code}"
    data = {
        'login': settings.NIKITA_LOGIN,
        'pwd': settings.NIKITA_PASSWORD,
        'id': id_string,
        'sender': settings.NIKITA_SENDER,
        'text': message,
        'phones': [phone_number],
    }
    
    # Добавляем тестовый флаг, если требуется
    if str(settings.NIKITA_TEST) == "1":
        data['test'] = "1"
    
    # Преобразование данных в XML
    xml_page = dicttoxml(data, custom_root='message',
                         item_func=lambda x: x[:-1], attr_type=False)
    
    # Логирование отправляемого XML-запроса
    print(f"Sending SMS request: {xml_page}")
    
    # Отправка запроса
    response = requests.post(
        settings.NIKITA_URL,
        data=xml_page, headers={'Content-Type': 'application/xml'}
    )
    
    # Логирование ответа
    print(f"Response status: {response.status_code}, Response body: {response.text}")
    
    # Преобразование ответа из XML в словарь
    response_dict = xmltodict.parse(response.text)
    status = response_dict['response']['status']
    
    # Проверка статуса ответа
    if status not in ('0', '11'):
        print(f"SMS sending failed. Status: {status}")
        return False
    
    # Сообщение успешно отправлено
    return True