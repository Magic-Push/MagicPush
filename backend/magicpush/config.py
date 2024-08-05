import os
from celery.schedules import crontab


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_TIMEZONE = 'UTC'
    CELERY_IMPORTS = 'magicpush.celery_tasks'
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
    CELERY_ONCE_URL = os.getenv('CELERY_ONCE_URL')
    CELERY_IGNORE_RESULT = True
    CELERYBEAT_SCHEDULE = {
        'notifier': {
            'task': 'magicpush.celery_tasks.notifier',
            'schedule': crontab(minute='*/1')
        },
        'run_billing': {
            'task': 'magicpush.celery_tasks.run_billing',
            'schedule': crontab(hour=0, minute=0)
        },
        'run_flow': {
            'task': 'magicpush.celery_tasks.run_flow',
            'schedule': crontab(minute='*/15')
        },
    }

    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 2

    APN_HOST = 'api.push.apple.com:443'
    FCM_HOST = 'https://fcm.googleapis.com/v1/'
    HMS_HOST = 'https://push-api.cloud.huawei.com/v1/'


class DevConfig(BaseConfig):
    APN_HOST = 'api.sandbox.push.apple.com:443'
