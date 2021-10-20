"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m3es^j#70cjif9=du4!*0j#2ti3oo^i@sr*)=wwnvie1uczv_4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False 

ALLOWED_HOSTS = [
    '127.0.0.1',
    'newspaper',
    '172.23.197.233',
    '172.23.199.73',
]

ACCOUNT_FORMS = {'signup': 'news.forms.BasicSignupForm'}


ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda a: "/posts/",
}

APSCHEDULER_RUN_NOW_TIMEOUT = 25


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # added app:
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_filters',
    'fpages',
    'news.apps.NewsConfig',
    'django_apscheduler',

    #allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
]

DEFAULT_FROM_EMAIL = 'artiom199821zxc@gmail.com'


ADMINS = [
    ('admin', 'ivan199821zxc@gmail.com'),
]

SITE_ID = 2

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # added decoretores
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',

]

LOGIN_URL = '/accounts/login/'

LOGOUT_REDIRECT_URL = '/posts/'

LOGIN_REDIRECT_URL = '/posts/<int:pk>/'

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'templates', 'allauth')],
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

TEMPLATE_CONTEXT_PROCESSORS = (
    "module.context_processors.site",
)

AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email sending django
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'artiom199821zxc'
EMAIL_HOST_PASSWORD = "none"
EMAIL_USE_TLS = True

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379' # указывает на URL брокера сообщений (Redis). По умолчанию он находится на порту 6379.
CELERY_RESULT_BACKEND = 'redis://localhost:6379' # указывает на хранилище результатов выполнения задач.
CELERY_ACCEPT_CONTENT = ['application/json'] # допустимый формат данных.
CELERY_TASK_SERIALIZER = 'json' # метод сериализации задач.
CELERY_RESULT_SERIALIZER = 'json' # метод сериализации результатов.

CAHES = {
    'default':{
        'TIMEOUT': 60,
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
    }
}


#time
USE_TZ = False

# internationalization
USE_I18N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version' : 1, # version at moment have be only 1
    'disable_existing_loggers' : False, # allow to disable existing logging system
    'style' : '{',
    'formatters' : {
        'simple': {
            'style': '{',
            'format' : '{asctime} {levelname} {message}' # format contain level of logging and message, asctime = occur time
        },
        'advanced' : {
            'style': '{',
            'format' : '{actime} {levelname} {pathname} {message}' 
        },
        'advanced_1' : {
            'style': '{',
            'format' : '{actime} {levelname} {pathname} {message} {exc_info} '
        },
        'advanced_2' : {
            'style': '{',
            'format' : '{actime} {levelname} {module} {message}'
        },
        'advanced_3' : {
            'style': '{',
            'format' : '{levelname} {module} {message}'
        }
    },
    'filters' : {
        'require_debug_true' : {
            '()' : 'django.utils.log.RequireDebugTrue', # filter which report DEBUG = TRUE
        },
        'require_debug_false' : {
            '()' : 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers' : {
        'console' : {
            'level' : 'DEBUG',
            'filters' : ['require_debug_true'],
            'class' : 'logging.StreamHandler',
            'formatter' : 'simple'
        }, 
        'console_1' : {
            'level' : 'WARNING',
            'filters' : ['require_debug_true'],
            'class' : 'logging.StreamHandler',
            'formatter' : 'advanced'
        },
        'console_2' : {
            'level' : 'ERROR',
            'filters' : ['require_debug_true'],
            'class' : 'logging.StreamHandler',
            'formatter' : 'advanced_1'
        },
        'general_log_file' : {
            'level' : 'INFO',
            'filters' : ['require_debug_false'],
            'class' : 'logging.FileHandler',
            'formatter' : 'advanced_2',
            'filename' : 'general.log',
        },
        'error_log_file' : {
            'level' : 'ERROR',
            'class' : 'logging.FileHandler',
            'formatter' : 'advanced_1',
            'filename' : 'errors.log',
        },
        'security_log_file' : {
            'level' : 'DEBUG',
            'class' : 'logging.FileHandler',
            'formatter' : 'advanced_1',
            'filename' : 'errors.log',
        },
        'mail_admins' : {
            'level' : 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'advanced',
        },
    },
    'loggers' : {
        'django' : {
            'handlers' : ['console', 'console_1', 'console_2', 'general_log_file'],
            'level' : 'DEBUG',
            'propagate' : True, # allow to get this messagge by other loggers
        },
        'django.request' : {
            'handlers' : ['error_log_file', 'mail_admins'],
            'level' : 'ERROR',
            'propagate' : True,
        },
        'django.server' : {
            'handlers' : ['error_log_file'],
            'level' : 'ERROR',
            'propagate' : True,
        },
        'django.template' : {
            'handlers' : ['error_log_file'],
            'level' : 'ERROR',
            'propagate' : True,
        },
        'django.db_backends' : {
            'handlers' : ['error_log_file'],
            'level' : 'ERROR',
            'propagate' : True,
        },
        'django.security' : {
            'handlers' : ['security_log_file'],
            'level' : 'DEBUG',
            'propagate' : True,
        },
    }
}