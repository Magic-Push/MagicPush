from . import health
from magicpush import celery_app


@health.route('/celery', methods=['GET'])
def celery_health():
    inspect = celery_app.control.inspect()

    # Ping the workers
    ping_responses = inspect.ping()

    if ping_responses:
        return "Celery is running.", 200
    else:
        return "Celery is not running. Workers did not respond to ping.", 500
