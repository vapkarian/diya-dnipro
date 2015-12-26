from psdnipro.settings import INSTALLED_APPS, DATABASES, TEMPLATES


INSTALLED_APPS.append('debug_toolbar')

DATABASES['default']['USER'] = '{DB_USER}'
DATABASES['default']['PASSWORD'] = '{DB_PASSWORD}'

TEMPLATES[0]['APP_DIRS'] = True
del TEMPLATES[0]['OPTIONS']['loaders']


DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
