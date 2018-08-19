#encoding: utf-8
# 配置文件
import os

database_uri={
    'mysql':'mysql+pymysql://root:123456@localhost:3306/fans_blog?charset=utf8',
    'postgre':'postgresql+py-postgresql://postgres:123456@localhost:5432/fans_blog',
    'default':'sqlite:////absolute/path/to/database'
}


class Config(object):
    """Base config class."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '67c9b34a90f47c8155e1eb30009e2964' or 'hard to guess string'
    #SECRET_KEY = os.urandom(24)

    
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND =False
    MAIL_USERNAME = 'zhu14623@163.com'
    MAIL_PASSWORD = '*****'
    MAIL_SUBJECT_PREFIX = '[Flask]'
    MAIL_SENDER = 'zhu14623@163.com'

    # Celery <--> RabbitMQ connection
    #CELERY_RESULT_BACKEND = "amqp://guest:guest@localhost:5672//"
    #CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    # SSL_REDIRECT = False
    # SQLALCHEMY_RECORD_QUERIES = True

    # FLASKY_POSTS_PER_PAGE = 20
    # FLASKY_FOLLOWERS_PER_PAGE = 50
    # FLASKY_COMMENTS_PER_PAGE = 30
    # FLASKY_SLOW_DB_QUERY_TIME = 0.5


    @staticmethod
    def init_app(app):
        pass



class DevelopmentConfig(Config):
    """Development config class."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = database_uri['mysql']
    # SQLALCHEMY_BINDS = 'mysql+pymysql://root:123456@localhost:3306/fans_blog?charset=utf8'

    #### Flask-Cache's config
    CACHE_TYPE = 'simple'

    # Flask-Assets's config
    # Can not compress the CSS/JS on Dev environment.
    ASSETS_DEBUG = True



class TestingConfig(Config):
    """Testing config class."""
    pass



class ProductionConfig(Config):
    """Production config class."""
    #DEBUG = True
    SQLALCHEMY_DATABASE_URI = database_uri['mysql']

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}