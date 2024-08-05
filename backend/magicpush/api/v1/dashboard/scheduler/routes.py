from . import scheduler
from magicpush import app
from magicpush.models import App, Notification, NotificationTranslation

import datetime
from dateutil import parser
from flask import jsonify, request
from flask_login import login_required, current_user


# get scheduled notifications
@scheduler.route('/<app_id>', methods=['GET'])
@login_required
def get_scheduled_notifications(app_id):
    from magicpush.database import db_session
    try:
        if current_user.is_admin:
            current_app = db_session.query(App).filter(App.id == app_id).first()
        else:
            current_app = db_session.query(App).filter(App.id == app_id, App.user_id == current_user.id).first()

        if current_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        start_date = parser.parse(request.args.get('start_date'))
        end_date = parser.parse(request.args.get('end_date'))

        notifications = db_session.query(Notification)\
            .filter(Notification.app_id == current_app.id)\
            .filter(Notification.scheduled_at >= start_date)\
            .filter(Notification.scheduled_at <= end_date)\
            .all()

        json = []
        for notification in notifications:
            json.append(notification.to_json())

        db_session.close()

        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500
