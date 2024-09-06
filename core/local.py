# from .env_reader import env
from .settings import BASE_DIR
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY =  os.environ.get('SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
