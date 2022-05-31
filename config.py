
class Config(object):
    DATABASE_CONNECT_OPTIONS = {}

    # Turn off Flask-SQLAlchemy event system
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
    SECRET_KEY = '+=gP/3-i8wy}Ug26AK8H'
    MYSQL_PASSWORD = 'DA#842488'
    MYSQL_DB = 'Inicdanse'
    DEBUG = True
    SECURITY_PASSWORD_SALT ='220801054250017055590434028109221748090'
    UPLOAD_FOLDER = '/static/Costumeimage'
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_MAX_FILES = 30
    DROPZONE_IN_FORM = True
    DROPZONE_UPLOAD_ON_CLICK = True
    DROPZONE_UPLOAD_ACTION = 'costume_blueprint.handle_upload'  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID = 'submit'
    DROPZONE_DEFAULT_MESSAGE="Deposez les imgages ici "
    DROPZONE_UPLOAD_MULTIPLE=True