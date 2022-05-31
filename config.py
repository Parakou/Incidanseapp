
class Config(object):
    DATABASE_CONNECT_OPTIONS = {}

    # Turn off Flask-SQLAlchemy event system
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = 'SECRET'

    @staticmethod
    def init_app(app):
        pass


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:DA#842488@192.168.2.9/Incidanse'


class DevelopmentConfig:
    """Statement for enabling the development environment"""
    # Define the database - we are working with
    SQLALCHEMY_DATABASE_URI = 'mysql://root:DA#842488@192.168.2.9/Incidanse'
    DEBUG = False


class TestingConfig:
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:DA#842488@192.168.2.9/Incidanse'
    MYSQL_HOST = '192.168.2.9'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'DA#842488'
    MYSQL_DB = 'Inicdanse'
    DEBUG = True


