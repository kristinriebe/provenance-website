import os
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Read values from a secret file, for use in production server environment
import yaml
try:
    with open(os.path.join(BASE_DIR,'custom_settings.yaml'), 'r') as f:
        custom = yaml.load(f)
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    raise
except yaml.YAMLError as e:
    print "Error reading YAML file: ", e
    raise
except:
    print "Unexpected error: ", sys.exc_info()[0]
    raise

# append path to prov-vo library package
sys.path.append(custom['prov_vo'])
sys.path.append(custom['vosi'])

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = custom['key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = custom['debug']

ALLOWED_HOSTS = custom['allowed_hosts']


# Application definition

INSTALLED_APPS = [
    'test_without_migrations', # needed for testing unmanaged models (with "managed=False")
    'core',
    'prov_vo.apps.ProvVoConfig',
    'raveprov',
    'vosi',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions', # for graphs!
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'provenance.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'provenance.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  os.path.join(BASE_DIR, 'provdb.sqlite3'),
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

# Logging setup
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log')
        }
    },
    'loggers': {
        'core': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'prov_vo': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'raveprov': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# custom settings for prov_vo app:
PROV_VO_CONFIG = {
    'namespaces': {
        "rave": "http://www.rave-survey.org/prov/",
        "org": "http://www.ivoa.net/documents/ProvenanceDM/ns/org/",
        "vo": "http://www.ivoa.net/documents/ProvenanceDM/ns/vo",

    },
    'provdalform': {
        'obj_id.help_text': "Please enter the identifier for an entity (e.g. rave:20030411_1507m23_001 or rave:20121220_0752m38_089) or an activity (e.g. rave:act_irafReduction)"
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR,'static/')
STATIC_URL = custom['static_url']
