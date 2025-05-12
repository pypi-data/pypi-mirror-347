# config.py

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from cores.utils.index import str_to_bool

# Load các biến môi trường từ file .env
load_dotenv()


@dataclass
class AccessToken:
    USER_SECRET_KEY = os.getenv("USER_SECRET_KEY", "")
    EXPIRES_IN = int(os.getenv("EXPIRES_IN", 8000))


class Config:
    SERVICE_MANAGEMENT_ID = os.getenv("SERVICE_MANAGEMENT_ID", "")

    APP_ENV = os.getenv("APP_ENV", "local")
    APP_DEBUG = str_to_bool(os.getenv("APP_DEBUG", "false"))
    APP_PORT = int(os.getenv("APP_PORT", 8000))
    SENTRY_ENABLE = str_to_bool(os.getenv("SENTRY_ENABLE", "false"))
    SENTRY_DNS = os.getenv("SENTRY_DNS", "")
    API_SYNC_KEY = os.getenv("API_SYNC_KEY", "sdfghuisfodhg")
    HOOK_API_KEY = os.getenv("HOOK_API_KEY", "sdfghuisfodhg")

    BASE_URL = os.getenv("BASE_URL", "http://proxy:8000/")
    AUTH_BASE_URL = os.getenv("AUTH_BASE_URL", "http://auth_service:8000/")
    PROFILE_BASE_URL = os.getenv(
        "PROFILE_BASE_URL", "http://profile_service:8000/"
    )
    USER_BASE_URL = os.getenv("USER_BASE_URL", "http://user_service:8000/")
    VOTE_BASE_URL = os.getenv("VOTE_BASE_URL", "http://vote_service:8000/")
    MANAGEMENT_BASE_URL = os.getenv(
        "MANAGEMENT_BASE_URL", "http://management_service:8016/"
    )
    NOTIFIER_BASE_URL = os.getenv("NOTIFIER_BASE_URL", "http://notifier:8000/")
    RESOURCE_BASE_URL = os.getenv(
        "RESOURCE_BASE_URL", "http://resource_service:8000/"
    )
    COLLABORATOR_BASE_URL = os.getenv(
        "COLLABORATOR_BASE_URL", "http://collaborator:8000/"
    )
    BOOKING_BASE_URL = os.getenv(
        "BOOKING_BASE_URL", "http://booking_service:8000/"
    )
    AUTHENTICATOR_BASE_URL = os.getenv(
        "AUTHENTICATOR_BASE_URL", "http://192.168.61.40:8022/"
    )
    SSO_BASE_URL = os.getenv("SSO_BASE_URL", "")

    BASE_SERVICE_ID = os.getenv("BASE_SERVICE_ID", "")
    AUTH_SERVICE_ID = os.getenv("AUTH_SERVICE_ID", "auth-service")
    PROFILE_SERVICE_ID = os.getenv("PROFILE_SERVICE_ID", "profile-service")
    USER_SERVICE_ID = os.getenv("USER_SERVICE_ID", "user-service")
    VOTE_SERVICE_ID = os.getenv("VOTE_SERVICE_ID", "competition-vote-service")
    NOTIFIER_SERVICE_ID = os.getenv("NOTIFIER_SERVICE_ID", "notifier-service")
    RESOURCE_SERVICE_ID = os.getenv("RESOURCE_SERVICE_ID", "resource-service")
    SSO_SERVICE_ID = os.getenv("SSO_SERVICE_ID", "sso-service")
    COLLABORATOR_SERVICE_ID = os.getenv(
        "COLLABORATOR_SERVICE_ID", "collaborator-service"
    )
    BOOKING_SERVICE_ID = os.getenv("BOOKING_SERVICE_ID", "booking-service")

    AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "")
    SECRET_KEY_FOR_MANAGEMENT = os.getenv("SECRET_KEY_FOR_MANAGEMENT", "")

    db_host = os.getenv("db_host", "")
    db_username = os.getenv("db_username", "")
    db_password = os.getenv("db_password", "")
    db_database = os.getenv("db_database", "")
    ECHO_DB_LOG = str_to_bool(os.getenv("ECHO_DB_LOG", "false"))
    FIRE_BASE_CRED = os.getenv("FIRE_BASE_CRED", "")

    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")
    RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
    RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "")
    RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "events")

    FILEBEAT_HOST = os.getenv("FILEBEAT_HOST", "filebeat")
    FILEBEAT_PORT = os.getenv("FILEBEAT_PORT", "5044")

    ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")
    ELASTICSEARCH_PORT = os.getenv("ELASTICSEARCH_PORT", "9200")
    ELASTICSEARCH_USERNAME = os.getenv("ELASTICSEARCH_USERNAME", "")
    ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD", "")

    MONGODB_USERNAME = os.getenv("MONGODB_USERNAME", "root")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "root")
    MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
    MONGODB_PORT = os.getenv("MONGODB_PORT", "27017")
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "my_database")
    MONGODB_AUTHENTICATION_DATABASE = os.getenv(
        "MONGODB_AUTHENTICATION_DATABASE", "admin"
    )

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))
    access_token = AccessToken


# config = Config()
