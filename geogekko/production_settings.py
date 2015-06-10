from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangostack',
        'HOST': '/opt/bitnami/postgresql',
        'PORT': '5432',
        'USER': 'bitnami',
        'PASSWORD': '78f22aeb2b'
    }
}

ELASTIC_SEARCH_HOST="http://localhost:9200/"