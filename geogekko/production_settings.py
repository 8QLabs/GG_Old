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

TEMPLATE_DIRS=('/opt/bitnami/apps/django/django_projects/geogekko/templates')

ELASTIC_SEARCH_HOST="http://localhost:9200/"