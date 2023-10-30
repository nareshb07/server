"""
Django settings for whatsapp_clone project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zl4hyafu=ky(m@r&0pbg7qfsro*@r=2r%-js7y3#pj0g8onwvi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SITE_ID = 12

# Application definition

INSTALLED_APPS = [
    'channels',
    'chats',
    'chats.apps.ChatsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'widget_tweaks',
    'crispy_forms',
    'django.contrib.sites',
    'storages',
    'payment',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 
    
    # Add the account middleware:
    # 'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'whatsapp_clone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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

# WSGI_APPLICATION = 'whatsapp_clone.wsgi.application'

ASGI_APPLICATION = 'whatsapp_clone.asgi.application'

# LEARN CHANNELS
CHANNEL_LAYERS = {  
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        #'ENGINE': 'django.db.backends.sqlite3',

        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
       
        'NAME': 'whatspp_v2',
        'USER': 'Naresh',
        'PASSWORD': '1243',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'chats.validator.SpaceValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    # 'content/static',
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")



MEDIA_URL = '/media/'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
}


ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True

# usename adpater
SOCIALACCOUNT_ADAPTER = 'chats.adapters.UsernameAccountAdapter'
# Connecting Existing Account
SOCIALACCOUNT_ADAPTER = 'chats.adapters.ConnectingAccountAdapter'




SOCIALACCOUNT_LOGIN_ON_GET=True


################# Email sending Credentials ##################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'messimowa11@gmail.com'
EMAIL_HOST_PASSWORD = '5kJVRMrdvqOc9j6H'
################# Email sending Credentials ##################

AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    #'django.contrib.auth.backends.ModelBackend',
    'chats.authentication.EmailAuthBackend',    
    'allauth.account.auth_backends.AuthenticationBackend',
]



AUTH_USER_MODEL = 'chats.User'

LOGIN_REDIRECT_URL = "/chat"

LOGOUT_REDIRECT_URL = "landingpage"

LOGIN_URL = '/login/'

AUTHENTICATION_FORM = 'django.contrib.auth.forms.AuthenticationForm'


ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True




# newly added
# ACCOUNT_SIGNUP_FORM_CLASSES = {
#     "Follower": "chats.forms.FollowerSignUpForm",
#     "Creator": "chats.forms.CreatorSignUpForm",
# }

# ACCOUNT_SIGNUP_VIEWS = {
#     "Follower": "chats.views.FollowerSignupView",
#     "Creator": "chats.views.CreatorSignupView",
# }


###############################################################
#############  PAYMENT  SETTINGS  #############################
###############################################################


PAYTM_MERCHANT_ID = 'your_merchant_id'
PAYTM_MERCHANT_KEY = 'your_merchant_key'
PAYTM_WEBSITE = 'WEBSTAGING'  # Change it to 'DEFAULT' in production


################################################################
#############  PAYMENT  SETTINGS  #############################
###############################################################




################################################################
#############  AWS #############################
###############################################################




DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'AKIA5OL74EB75LR3MDFJ'
AWS_SECRET_ACCESS_KEY = 'kObq9YGRrFI7stYD013NwtrcaXjkuABPU0WMkkxg'
AWS_STORAGE_BUCKET_NAME = 'nareshdjagnotest'
AWS_S3_REGION_NAME = 'ap-south-1'  # e.g., 'us-west-2'


################################################################
#############  AWS                #############################
###############################################################



################################################################
#############  Razor pay Credentials               #############
################################################################
RAZORPAY_KEY_ID = 'rzp_test_JXDhWdMqazVxVV'
RAZORPAY_KEY_SECRET = 'cq7X1NctUA5IvNGuMUgMkux2'
################################################################
#############  Razor pay Credentials    ########################
################################################################

