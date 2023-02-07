import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False #token based
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

class DevelopmentConfig(Config):
    DEBUG = True
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "develdb.sqlite3")
    SECRET_KEY = "11f6a704906b6e3b2bb2d3f3100f6378" #Random generation
    SECURITY_PASSWORD_HASH = "bcrypt" #Hashing Algorithm
    SECURITY_PASSWORD_SALT = "16e29a5d1e2662833e87cceb242c0e8c" #Random generation
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    CELERY_TIMEZONE = "Asia/Kolkata"
    REDIS_URL = "redis://localhost:6379/0"
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 9
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "priyankamazumdar0612@gmail.com"
    SENDER_PASSWORD = ""


class ProductionConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "proddb.sqlite3")
    SECRET_KEY = os.getenv("SECRET_KEY", None)
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = os.getenv("SECRET_PASSWORD_SALT", None)
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    CELERY_TIMEZONE = "Asia/Kolkata"
    REDIS_URL = "redis://localhost:6379"
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 9
    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "priyankamazumdar0612@gmail.com"
    SENDER_PASSWORD = ""
