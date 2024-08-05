from . import rest
from magicpush import app, db
from magicpush.celery_tasks import send_push
from magicpush.schemas import SendSchema, SendOutputSchema, ValueSchema, EventSchema
from magicpush.models import (App, AppUser, AppUserKey, AppUserValue, Notification, NotificationTranslation, Flow,
                              ActiveFlow)

import os
import jwt
from pathlib import Path
from pywebpush import webpush
from flask import jsonify, request, g


@rest.before_request
def before_request():
    if 'Authorization' in request.headers:
        token = request.headers.get('Authorization')
        if token is not None and 'Bearer' in token:
            try:
                token = token[token.index('Bearer') + 7:]

                dir = os.path.dirname(__file__)
                public_key = Path(dir, '../../../storage/private/id_rsa.pub')
                with open(public_key) as f:
                    decoded = jwt.decode(token, f.read(), algorithms='RS256')

                g.selected_app = App.query.filter_by(id=decoded['id']).first()

                db.session.commit()
            except jwt.exceptions.ExpiredSignatureError as e:
                print('Expired')
                return jsonify({'message': 'Unauthorized'}), 401
            except jwt.exceptions.InvalidTokenError as e:
                print('Invalid')
                return jsonify({'message': 'Unauthorized'}), 401
    else:
        return jsonify({'message': 'Unauthorized'}), 401


@rest.route('/send', methods=['POST'])
@rest.input(SendSchema)
@rest.output(SendOutputSchema)
def send():
    from magicpush.database import db_session
    try:
        if 'title' in request.json and 'message' in request.json:
            new_notification = Notification()
            new_notification.app_id = g.selected_app.id
            new_notification.name = request.json.get('name') \
                if 'name' in request.json else None
            new_notification.default_title = request.json.get('title') \
                if 'title' in request.json else None
            new_notification.default_message = request.json.get('message') \
                if 'message' in request.json else None
            new_notification.image = request.json.get('image') \
                if 'image' in request.json else None
            new_notification.action = request.json.get('action') \
                if 'action' in request.json else None
            new_notification.scheduled_at = request.json.get('scheduled_at') \
                if 'scheduled_at' in request.json else None
            new_notification.repeat = request.json.get('repeat') \
                if 'repeat' in request.json else False
            new_notification.repeat_interval = request.json.get('repeat_interval') \
                if 'repeat_interval' in request.json else None
            new_notification.recipients = (str(request.json.get('recipients')).replace('[', '')
                                           .replace(']', '').replace('\'', '')) \
                if 'recipients' in request.json else 'all'
            new_notification.sent = True
            db_session.add(new_notification)
            db_session.commit()

            if 'translations' in request.json:
                for translation in request.json.get('translations'):
                    new_notification_translation = NotificationTranslation()
                    new_notification_translation.notification_id = new_notification.id
                    new_notification_translation.language = translation.get('language')
                    new_notification_translation.title = translation.get('title')
                    new_notification_translation.message = translation.get('message')
                    db_session.add(new_notification_translation)
                    db_session.commit()

            send_push.delay(new_notification.id)

            json = new_notification.to_json()
            db_session.close()
            return jsonify(json), 201
        else:
            db_session.close()
            return jsonify({'message': 'Data is missing'}), 400
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@rest.route('/users/<app_user_hash>/values', methods=['POST'])
@rest.input(ValueSchema)
def register_value(app_user_hash):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.id == g.selected_app.id).first()

        if selected_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        app_user = db_session.query(AppUser)\
            .filter(AppUser.hash == app_user_hash, AppUser.app_id == selected_app.id)\
            .first()

        if app_user is None:
            db_session.close()
            return jsonify({'message': 'App user not found'}), 404

        if 'key' in request.json and 'value' in request.json:
            key = request.json.get('key')
            value = request.json.get('value')

            app_user_key = db_session.query(AppUserKey)\
                .filter(AppUserKey.app_user_id == app_user.id, AppUserKey.key == key)\
                .first()

            if app_user_key is None:
                app_user_key = AppUserKey()
                app_user_key.app_user_id = app_user.id
                app_user_key.key = key
                db_session.add(app_user_key)
                db_session.commit()

            app_user_value = db_session.query(AppUserValue)\
                .filter(AppUserValue.app_user_id == app_user.id, AppUserValue.key == key)\
                .first()

            if app_user_value is not None:
                if app_user_value.value == str(value):
                    db_session.close()
                    return jsonify({'message': 'Ok'}), 200

            app_user_value = AppUserValue()
            app_user_value.app_user_id = app_user.id
            app_user_value.key = key
            app_user_value.value = str(value)
            db_session.add(app_user_value)
            db_session.commit()

        db_session.close()
        return jsonify({'message': 'Ok'}), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@rest.route('/users/<app_user_hash>/events', methods=['POST'])
@rest.input(EventSchema)
def register_event(app_user_hash):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.id == g.selected_app.id).first()

        if selected_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        app_user = db_session.query(AppUser)\
            .filter(AppUser.hash == app_user_hash, AppUser.app_id == selected_app.id)\
            .first()

        if app_user is None:
            db_session.close()
            return jsonify({'message': 'App user not found'}), 404

        if 'event' in request.json:
            event = request.json.get('event')

            # check if event is associated with a notification flow
            flow = db_session.query(Flow)\
                .filter(Flow.app_id == selected_app.id, Flow.event == event, Flow.enabled == True)\
                .first()

            if flow is not None:
                # check if app user is already in active flow
                active_flow = db_session.query(ActiveFlow)\
                    .filter(ActiveFlow.app_user_id == app_user.id, ActiveFlow.flow_id == flow.id)\
                    .first()

                if active_flow is None:
                    active_flow = ActiveFlow()
                    active_flow.app_user_id = app_user.id
                    active_flow.flow_id = flow.id
                    db_session.add(active_flow)
                    db_session.commit()
        db_session.close()
        return jsonify({'message': 'Ok'}), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500

