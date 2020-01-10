import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'communityc_db_v3',
        'USER': 'postgres',
        'PASSWORD': 'Seneevo1992',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


DEBUG = True