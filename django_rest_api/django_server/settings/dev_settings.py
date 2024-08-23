import os
from .base_settings import *
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

DEBUG=True

SECRET_KEY=os.getenv('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DEV_DATABASE_NAME'),
        'USER': os.getenv('DEV_DATABASE_USER'),
        'PASSWORD': os.getenv('DEV_DATABASE_PASSWORD'),
        'HOST': os.getenv('DEV_DATABASE_HOST'),
        'PORT': os.getenv('DEV_DATABASE_PORT'),
    }
}
