from distutils.command.config import config
from distutils.debug  import DEBUG


class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER= 'tdea'
    MYSQL_PASSWORD='54321'
    MYSQL_DB='api-flask'

config={
    'development': DevelopmentConfig
}