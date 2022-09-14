import os
from dotenv import load_dotenv
from datetime import timedelta  # add

# .envファイルの内容を読み込見込む
if os.environ.get("DJANGO_SETTINGS_MODULE") == 'config.settings.dev':
    load_dotenv(".env.dev")
elif os.environ.get("DJANGO_SETTINGS_MODULE") == 'config.settings.prod':
    load_dotenv(".env.prod")


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',  # Django Rest Framework
    'djoser',  # Django djoser JWT
    'corsheaders',  # Django CORS Headers
    'django_filters',  # django-filter
    'django_celery_beat',  # django_celery_beat
    'django_celery_results',  # django_celery_results

    # my-app
    'apps.accounts',
    'apps.votes',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Django CORS Headers
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


AUTH_USER_MODEL = 'accounts.CustomUser'


# ローカル確認用
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# 本番環境用
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'vote.app.system@gmail.com'
EMAIL_HOST_PASSWORD = 'xsdcrxtcnfnaifkd'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'vote.app.system@gmail.com'


# rest_framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    # 認証が必要
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# simple_jwt
SIMPLE_JWT = {
    # JWT認証用のプレフィックスを設定する
    'AUTH_HEADER_TYPES': ('JWT',),
    # トークンの持続時間の設定
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=100)

}
# django-templated-mail
DOMAIN = '0.0.0.0:8080/#'


# djoser
DJOSER = {
    # メールアドレスでログイン
    'LOGIN_FIELD': 'email',
    # アカウント本登録メール
    'SEND_ACTIVATION_EMAIL': True,
    # アカウント本登録完了メール
    'SEND_CONFIRMATION_EMAIL': True,
    # メールアドレス変更完了メール
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    # パスワード変更完了メール
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    # アカウント登録時に確認用パスワード必須
    'USER_CREATE_PASSWORD_RETYPE': True,
    # メールアドレス変更時に確認用メールアドレス必須
    'SET_USERNAME_RETYPE': True,
    # パスワード変更時に確認用パスワード必須
    'SET_PASSWORD_RETYPE': True,
    # アカウント本登録用URL
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    # メールアドレスリセット完了用URL
    'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
    # メールアドレスリセット時のメールアドレスバリデーション
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    # パスワードリセット完了用URL
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    # カスタムユーザー用シリアライザー
    'SERIALIZERS': {
        'user_create_password_retype': 'apps.accounts.serializers.MyUserCreatePasswordRetypeSerializer',
    },
    # メール内容変更
    'EMAIL': {
        # アカウント本登録
        'activation': 'apps.accounts.email.ActivationEmail',
        # アカウント本登録完了
        'confirmation': 'apps.accounts.email.ConfirmationEmail',
        # パスワードリセット
        'password_reset': 'apps.accounts.email.PasswordResetEmail',
        # パスワードリセット完了
        'password_changed_confirmation': 'apps.accounts.email.PasswordChangedConfirmationEmail',
        # メールアドレスリセット
        'username_reset': 'apps.accounts.email.UsernameResetEmail',
        # メールアドレスリセット完了
        'username_changed_confirmation': 'apps.accounts.email.UsernameChangedConfirmationEmail',
    },
}

# Django CORS Headers
CORS_ORIGIN_WHITELIST = os.environ.get("CORS_ORIGIN_WHITELIST").split(" ")


# celery,redis
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/1')
CELERY_TIMEZONE = 'Asia/Tokyo'
CELERY_RESULT_BACKEND = 'django-db'
