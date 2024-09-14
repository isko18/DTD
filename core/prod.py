from .env_reader import env

SECRET_KEY =  env('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_USER_PASSWORD"),
        'HOST': env('DB_HOST'),
        'PORT': env("DB_PORT"),
    }
}