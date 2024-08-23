import os
from .settings import *
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

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
