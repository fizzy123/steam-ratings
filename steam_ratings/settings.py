DEBUG = False
TESTING = False
CSRF_ENABLED = True
SECRET_KEY = '25f94dba-91d7-4355-87c8-1581ec245034'

POSTGRES = {
    'user': 'steam_ratings',
    'pw': '85aed77c-49a2-40e0-b86e-1611f167afb3',
    'db': 'steam_ratings',
    'host': '10.180.184.6'
}

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(POSTGRES['user'], POSTGRES['pw'], POSTGRES['host'], POSTGRES['db'])

PASSWORD_SCHEMES = [
    'pbkdf2_sha512',
    'md5_crypt'
]
TRAP_HTTP_EXCEPTIONS=True
