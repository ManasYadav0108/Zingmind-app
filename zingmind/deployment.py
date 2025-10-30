import os 
from .settings import *
from .settings import BASE_DIR
import pymysql

pymysql.install_as_MySQLdb()

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME'],
    "127.0.0.1",
    "localhost",
]
CSRF_TRUSTED_ORIGINS = ['*','https://'+ os.environ['WEBSITE_HOSTNAME']]
DEBUG = False


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE ='whitenoise.storage.compressedManifeststaticfilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')


# Get the MySQL connection string from environment variable
connection_string = os.environ['AZURE_MYSQL_CONNECTIONSTRING']

# Split by semicolon and create a dictionary of parameters
parameters = dict(
    pair.strip().split('=', 1)
    for pair in connection_string.split(';') if '=' in pair
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("zingmind_hrms" ),
        "USER": os.environ.get("root"),
        "PASSWORD": os.environ.get("Sharad@19"),
        "HOST": os.environ.get("localhost"),
        "PORT": os.environ.get("3306"),
    }
}