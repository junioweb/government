import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '*g6qz9e7=b@8p#8@vz=t#3b9acpggqz9h5)4kn6#9c(!7@e1qv'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    ENV = 'dev'
    SECRET_KEY = '4hyt%4p8gyo7ooyj7kayrih^^#h8x+eccg+etgi3wtah)_8%d4'


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    ENV = 'staging'
    SECRET_KEY = '^+%(yijo0$i^6!1%ij4(gwnmw^hkt6&o3&gxu7(n!yyzjf+ce$'


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    ENV = 'prod'
    SECRET_KEY = 'u0gcqj=*8m$%2c3_5-5(qf%z0bhnzj_2#4nvnk6zbser*_d@18'


config = {
    'dev': 'application.config.DevelopmentConfig',
    'staging': 'application.config.TestingConfig',
    'prod': 'application.config.ProductionConfig',
    'default': 'application.config.DevelopmentConfig'
}


def configure_app(app):
    config_name = os.getenv('STAGE', 'default')
    app.config.from_object(config[config_name])
