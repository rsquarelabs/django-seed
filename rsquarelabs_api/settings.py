"""
Django settings for rsquarelabs_api project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

BROKER_URL = 'amqp://guest:guest@localhost:5672//'

from datetime import  datetime, timedelta

from .config import dev as SET
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


CONFIG_DIR = os.path.join(BASE_DIR, 'configs')
LOGFILE_NAME = "rsquarelabs"
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@hn33bo@rd%r318eodg%itfp3@z+fx$&q0(cs-&p1o3_i8h(99'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['localhost']


SEND_BROKEN_LINK_EMAILS = True

ADMINS = (
    ('Ravi', 'demo@rsquarelabs.xyz'), ('Example', 'example@rsquarelabs.xyz'),
)
MANAGERS = ADMINS

EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"  # Override your existing EMAIL_BACKEND with the following line:
SERVER_EMAIL = 'admin@example.com'


''' Mandrill Email - Regarding the email functionality '''
MANDRILL_API_KEY = SET.MANDRILL_API_KEY




# AUTH_USER_MODEL = "restful.users.User"
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'core',
    'bootstrapform',
    'restful',
    'rest_framework',
     'rest_framework.authtoken',
    # 'rest_framework_swagger',
    'djcelery',
    'djrill',
]



## caching middleware added
## https://docs.djangoproject.com/en/1.9/topics/cache/#the-per-site-cache
MIDDLEWARE_CLASSES = [
    'django.middleware.cache.UpdateCacheMiddleware', # needed for cache | this must be first
    'django.middleware.common.BrokenLinkEmailsMiddleware', # should be placed on top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', # needed for cache | this must be last

]


# https://niwinz.github.io/django-redis/latest/#_configure_as_cache_backend
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


# https://niwinz.github.io/django-redis/latest/#_configure_as_session_backend
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

ROOT_URLCONF = 'rsquarelabs_api.urls'


#CUSTOM_USER_MODEL = "restful.users.models.User"

AUTHENTICATION_BACKENDS = ('core.backend.CustomModelBackend',)



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(os.path.dirname(__file__),'../website/templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]






REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer', #enables browsable api
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
         'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',

    ),
    'PAGE_SIZE': 8,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'PAGINATE_BY': 8,
    'PAGINATE_BY_PARAM': 'page_size',


    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day', # this is the reason they have to register to us :D
        'user': '1000/day'
    }
}


JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(days=7), #token expires in 7 days
    'JWT_AUTH_HEADER_PREFIX': 'JWT', # this should be sent in the headers of AngularJS eg: 'JWT <token>',
    'JWT_VERIFY': True,
}


WSGI_APPLICATION = 'rsquarelabs_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'rsquarelabs_api1',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'postgres',
            'PASSWORD': 'welcome',
            'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
            'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_PATH = os.path.join(os.path.dirname(__file__),'../website/assets')
STATICFILES_DIRS = (
    STATIC_PATH,
)
STATIC_URL = '/assets/'



# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '%s/%s.log' %(LOGS_DIR,LOGFILE_NAME),
            'formatter': 'verbose'
        },

        # Include the default Django email handler for errors
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            # But the emails are plain text by default - HTML is nicer
            'include_html': True,
        },
    },
    'loggers': {
        # Again, default Django configuration to email unhandled exceptions
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Might as well log any errors anywhere else in Django
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        # Your own app - this assumes all your logger names start with "restful."
        'core': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'restful': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },


    }
}

