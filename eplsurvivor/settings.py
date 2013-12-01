# Django settings for eplsurvivor project.

import os.path
import socket

DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

ADMINS = (
    ('Ben Edwards', 'ben@benedwards.co.nz'),
)

DEFAULT_FROM_EMAIL = 'EPL Survivor <mailer@eplsurvivor.com>'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ben_eplsurvivor',                      # Or path to database file if using sqlite3.
        'USER': 'ben',                      # Not used with sqlite3.
        'PASSWORD': 'hfzVMSNv2MtVnBAG',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.eplsurvivor.com']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-nz'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "media") 

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = os.path.join(os.path.dirname(__file__), "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    os.path.join(os.path.dirname(__file__), "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'v5ps_uy$%dwudrhwfngr@b_m6xt%l8r30#q396r+al*wr_z_&@'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'eplsurvivor.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'eplsurvivor.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'survivor.context_processors.my_groups',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'survivor',
    'sorl.thumbnail',
    'chronograph',
    'registration',
    'social_auth',
)

#SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SALESFORCE_CONSUMER_KEY     = '3MVG99qusVZJwhsnmdmjq1uHdUrHw7YM6LakYhCxhvP3IMzoLXUB_cjFdpUhGMttiN7ooMHs3sTIF6emzDyzh'
SALESFORCE_CONSUMER_SECRET  = '2335697909761120514'
SALESFORCE_INSTANCE_URL     = 'https://eu2.salesforce.com/services/data/v29.0/'
SALESFORCE_POST_GROUP_URL   = SALESFORCE_INSTANCE_URL + 'chatter/feeds/record/0F9b0000000PYVU/feed-items'
SALESFORCE_HEADERS          = {'Authorization': 'Bearer 00Db0000000agC7!AQUAQIfaqgWzGeGuo1oUXAZbAqZgyso.tiQTNjWbNRXm1xN_8iAwiWCnZdRdtkEW9bV5RMDjUA8KmM33jIaeL1B4M0imas3A', 'content-type': 'application/json'}

FACEBOOK_APP_ID                 = '1375158226069437'
FACEBOOK_API_SECRET             = '72e8ecda7260fd146b4c9159f15367c1'
FACEBOOK_EXTENDED_PERMISSIONS   = ['email']

GOOGLE_OAUTH2_CLIENT_ID      = '600895131807-048uhp67v2p8j5m35l16dbaerht3lqri.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET  = 'vHfsgx6XgppW5C6zkEMkk4Yl'

LOGIN_URL           = '/'
LOGIN_REDIRECT_URL  = '/'