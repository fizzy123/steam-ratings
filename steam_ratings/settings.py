import os

DEBUG = False
TESTING = False
CSRF_ENABLED = True

POSTGRES = {
    'user': 'steam_ratings',
    'pw': os.environ['DB_PW'],
    'db': 'steam_ratings',
    'host': '10.180.184.6'
}

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(POSTGRES['user'], POSTGRES['pw'], POSTGRES['host'], POSTGRES['db'])

PASSWORD_SCHEMES = [
    'pbkdf2_sha512',
    'md5_crypt'
]
TRAP_HTTP_EXCEPTIONS=True
