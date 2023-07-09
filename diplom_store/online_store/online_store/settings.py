import os
from decouple import config
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

DEFAULT_CHARSET = 'utf-8'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool, default=False)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', config('ALLOWED_HOSTS', default='localhost')]

USER_ADMIN = config('USER_ADMIN')
EMAIL = config('EMAIL')
PASSWORD = config('PASSWORD')
ANONYMOUS_USER = config('ANONYMOUS_USER')
ANONYMOUS_USER_PASSWORD = config('ANONYMOUS_USER_PASSWORD')
CART_SESSION_ID = 'cart'

FIXTURE_DIRS = ['online_store/tests/fixtures/']

AUTH_USER_MODEL = 'account.User'

CSRF_FAILURE_VIEW = 'online_store.views.error_403'

SWAGGER_SETTINGS = {
    "DEFAULT_MODEL_RENDERING": "example"
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_filters',
    'frontend.apps.FrontendConfig',
    'settings.apps.SettingsConfig',
    'catalog.apps.CatalogConfig',
    'cart.apps.CartConfig',
    'order.apps.OrderConfig',
    'payment.apps.PaymentConfig',
    'product.apps.ProductConfig',
    'tag.apps.TagConfig',
    'account.apps.AccountConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', #добавлено для локализации
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8080']

ROOT_URLCONF = 'online_store.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'temp')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'cart.context_processor_cart.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'online_store.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, config('DB_NAME', default='db.sqlite3')),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT')
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    # 'DEFAULT_PERMISSION_CLASSES': [
    #         'rest_framework.permissions.IsAuthenticated',
    #     ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 8
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

# LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

SHORT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'frontend')]

LOGOUT_REDIRECT_URL = '/'

# Media directory in the root directory
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_AGE = 30 * 24 * 60 * 60

PAYMENT_METHODS = (
    (1, _("Online from a random someone else's account")),
    (2, _('Online card')),
)

SHIPPING_METHODS = (
    (1, _('Standard Shipping')),
    (2, _('Express Shipping')),
)

ORDER_STATUSES = (
    (1, _('Paid')),
    (2, _('Payment error')),
    (3, _('Process')),
)

FILTER_MIN_PRICE = 1
FILTER_MAX_PRICE = 500000
FILTER_CURRENT_FROM_PRICE = 1000
FILTER_CURRENT_TO_PRICE = 20000


EXPRESS_SHIPPING_COST = 500.00
STANDARD_SHIPPING_COST = 200.00
MIN_AMOUNT_FREE_SHIPPING = 2000.00
