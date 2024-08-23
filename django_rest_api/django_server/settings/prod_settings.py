import os
from .base_settings import *
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

DEBUG=False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

SECRET_KEY=os.getenv('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PROD_DATABASE_NAME'),
        'USER': os.getenv('PROD_DATABASE_USER'),
        'PASSWORD': os.getenv('PROD_DATABASE_PASSWORD'),
        'HOST': os.getenv('PROD_DATABASE_HOST'),
        'PORT': os.getenv('PROD_DATABASE_PORT'),
    }
}
