import requests

import xmltodict

from datetime import datetime

from django.conf import settings

from dicttoxml import dicttoxml


def send_nikita_sms(user, phone_number=None):
    if not settings.NIKITA_URL:
        return False
    id_string = '%s%d' % (user.id, datetime.now().timestamp())
    if not phone_number:
        phone_number = user.phone_number
    user.generate_and_save_verification_code()
    message = f"Ваш код верификации: {user.verification_code}"
    data = {
        'login': settings.NIKITA_LOGIN,
        'pwd': settings.NIKITA_PASSWORD,
        'id': id_string,
        'sender': settings.NIKITA_SENDER,
        'text': message,
        'phones': [phone_number],
    }
    if settings.NIKITA_TEST:
        data['test'] = "1"
    xml_page = dicttoxml(data, custom_root='message',
                     item_func=lambda x: x[:-1], attr_type=False)
    response = requests.post(
        settings.NIKITA_URL,
        data=xml_page, headers={'Content-Type': 'application/xml'}
    )
    response_dict = xmltodict.parse(response.text)
    status = response_dict['response']['status']
    if status not in ('0', '11'):
        # TODO: add error handle
        return False
    return True
