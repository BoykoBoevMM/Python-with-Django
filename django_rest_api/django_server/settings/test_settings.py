import os
from .base_settings import *
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path=dotenv_path)

DEBUG=False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

SECRET_KEY=os.getenv('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('TEST_DATABASE_NAME'),
        'USER': os.getenv('TEST_DATABASE_USER'),
        'PASSWORD': os.getenv('TEST_DATABASE_PASSWORD'),
        'HOST': os.getenv('TEST_DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('TEST_DATABASE_PORT', 5433),
    }
}
