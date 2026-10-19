import os

# NOTE: 無いと Did you install mysqlclient? と煽られます。
import pymysql

from .settings import *

pymysql.install_as_MySQLdb()

DEBUG = False

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# App Service は HTTPS で公開するので、 cookie は HTTPS のときだけ送ります。
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Configure the domain name using the environment variable
# that Azure automatically creates for us.
ALLOWED_HOSTS = [os.environ["WEBSITE_HOSTNAME"]] if "WEBSITE_HOSTNAME" in os.environ else []

# NOTE: App Service は HTTPS を手前で終端し、 X-Forwarded-Proto を付けて転送します。
#       これを信頼して HTTPS と判定させ、 HTTP で来たら HTTPS へリダイレクトします。
#       (HTTPS と判定できるので、 Django 4.0 以降の Origin チェックも通ります。)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
# NOTE: まずは短めの1時間にしています。
#       *.azurewebsites.net は自分のドメインではないので subdomains や preload は付けません。
SECURE_HSTS_SECONDS = 3600

# WhiteNoise configuration
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Add whitenoise middleware after the security middleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# NOTE: この設定はいろんなサイトに記載されているが、 Missing staticfiles manifest entry エラーを引き起こす。
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Configure Postgres database; the full username is username@servername,
# which we construct using the DBHOST value.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["DJANGO_DATABASE_NAME"],
        "USER": os.environ["DJANGO_DATABASE_USER"],
        "PASSWORD": os.environ["DJANGO_DATABASE_PASSWORD"],
        "HOST": os.environ["DJANGO_DATABASE_SERVER"],
        "PORT": "3306",
        # なんだこれ? と思うだろうけれど、 AppService 用の設定なので脳死で書く。
        "OPTIONS": {"ssl": {"ssl-ca": "/var/www/html/BaltimoreCyberTrustRoot.crt.pem"}},
    }
}
