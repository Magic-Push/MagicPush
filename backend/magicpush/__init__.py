from celery import Celery
from apiflask import APIFlask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = APIFlask(__name__, instance_relative_config=True)
    app.config.from_object('magicpush.config.BaseConfig')

    CORS(app, supports_credentials=False, send_wildcard=True)

    load_dotenv()

    return app


def celery_init_app(app: APIFlask) -> Celery:
    celery = Celery(
        app.import_name,
        broker=app.config.get('CELERY_BROKER_URL')
    )
    celery.conf.ONCE = {
        'backend': 'celery_once.backends.Redis',
        'settings': {
            'url': app.config.get('CELERY_ONCE_URL'),
            'default_timeout': 60 * 60
        }
    }
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract =  True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


app = create_app()

celery_app = celery_init_app(app)

login_manager = LoginManager(app)

db = SQLAlchemy(app)

from magicpush.models import *

migrate = Migrate(app, db)

from magicpush.api.v1.sdk import sdk
from magicpush.api.v1.rest import rest
from magicpush.api.v1.health import health
from magicpush.api.v1.dashboard.apps import apps
from magicpush.api.v1.dashboard.flow import flow
from magicpush.api.v1.dashboard.user import users
from magicpush.api.v1.dashboard.admin import admin
from magicpush.api.v1.dashboard.scheduler import scheduler
from magicpush.api.v1.dashboard.statistics import statistics
from magicpush.api.v1.dashboard.notifications import notifications

app.register_blueprint(sdk, url_prefix='/api/v1/sdk')
app.register_blueprint(rest, url_prefix='/api/v1/rest')
app.register_blueprint(apps, url_prefix='/api/v1/apps')
app.register_blueprint(flow, url_prefix='/api/v1/flows')
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(admin, url_prefix='/api/v1/admin')
app.register_blueprint(health, url_prefix='/api/v1/health')
app.register_blueprint(scheduler, url_prefix='/api/v1/scheduler')
app.register_blueprint(statistics, url_prefix='/api/v1/statistics')
app.register_blueprint(notifications, url_prefix='/api/v1/notifications')

if __name__ == '__main__':
    app.run()
