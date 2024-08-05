from . import sdk
from magicpush import app
from magicpush.helpers.encryption import Encryption
from magicpush.models import App, AppUserKey, AppUser, AppUserValue, Flow, ActiveFlow, AppUserNotification

import datetime
from flask import request, jsonify


@sdk.route('/app-by-hash/<app_hash>', methods=['GET'])
def get_app_by_hash(app_hash):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.hash == app_hash).first()

        if selected_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        if selected_app.vapid_public_key is None:
            private_key_pem, public_key_pem = Encryption.generate_vapid_keys()
            selected_app.vapid_public_key = public_key_pem
            selected_app.vapid_private_key = private_key_pem
            db_session.commit()

        vapid_public_key = selected_app.vapid_public_key

        json = {
            'hash': selected_app.hash,
            'name': selected_app.name,
            'website_url': selected_app.website_url,
            'widget_color': selected_app.widget_color if selected_app.widget_color else '#8b5cf6',
            'notification_groups': selected_app.notification_groups.split(',')
            if selected_app.notification_groups else ['functional','marketing'],
            'vapid_public_key': vapid_public_key
        }

        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@sdk.route('/app-user/<app_hash>/<app_user_hash>', methods=['GET'])
def get_app_user(app_hash, app_user_hash):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.hash == app_hash).first()

        if selected_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        selected_app_user = db_session.query(AppUser)\
            .filter(AppUser.hash == app_user_hash, AppUser.app_id == selected_app.id)\
            .first()

        if selected_app_user is None:
            db_session.close()
            return jsonify({'message': 'App user not found'}), 404

        json = selected_app_user.to_json()
        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@sdk.route('/app-user-from-endpoint/<endpoint>', methods=['GET'])
def get_app_user_from_endpoint(endpoint):
    from magicpush.database import db_session
    try:
        app_user = db_session.query(AppUser).filter(AppUser.web_push_endpoint == endpoint).first()

        if app_user is None:
            db_session.close()
            return jsonify({'message': 'App user not found'}), 404

        json = app_user.to_json()
        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


# register app user save fcm/apn token
@sdk.route('/app-user/<app_hash>', methods=['POST'])
def create_app_user(app_hash):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.hash == app_hash).first()

        if selected_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        app_user = AppUser()
        app_user.app_id = selected_app.id
        app_user.parent_id = request.json.get('parent_id') \
            if 'parent_id' in request.json else None
        app_user.fcm_token = request.json.get('fcm_token') \
            if 'fcm_token' in request.json else None
        app_user.apn_device_token = request.json.get('apn_device_token') \
            if 'apn_device_token' in request.json else None
        app_user.web_push_endpoint = request.json.get('web_push_endpoint') \
            if 'web_push_endpoint' in request.json else None
        app_user.web_push_auth = request.json.get('web_push_auth') \
            if 'web_push_auth' in request.json else None
        app_user.web_push_p256dh = request.json.get('web_push_p256dh') \
            if 'web_push_p256dh' in request.json else None
        app_user.language = request.json.get('language') \
            if 'language' in request.json else None
        app_user.notification_groups = (str(request.json.get('notification_groups'))
                                        .replace('[', '').replace(']', '')
                                        .replace('"', '')) \
            if 'notification_groups' in request.json else None
        db_session.add(app_user)
        db_session.commit()

        json = app_user.to_json()
        db_session.close()
        return jsonify(json), 201
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


# update app user fcm/apn token
@sdk.route('/app-user/<app_hash>/<app_user_hash>', methods=['PUT'])
def update_app_user(app_hash, app_user_hash):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.hash == app_hash).first()

        if selected_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        selected_app_user = db_session.query(AppUser)\
            .filter(AppUser.hash == app_user_hash, AppUser.app_id == selected_app.id)\
            .first()

        if selected_app_user is None:
            db_session.close()
            return jsonify({'message': 'App user not found'}), 404

        selected_app_user.fcm_token = request.json.get('fcm_token') \
            if 'fcm_token' in request.json else selected_app_user.fcm_token
        selected_app_user.apn_device_token = request.json.get('apn_device_token') \
            if 'apn_device_token' in request.json else selected_app_user.apn_device_token
        selected_app_user.web_push_endpoint = request.json.get('web_push_endpoint') \
            if 'web_push_endpoint' in request.json else selected_app_user.web_push_endpoint
        selected_app_user.web_push_auth = request.json.get('web_push_auth') \
            if 'web_push_auth' in request.json else selected_app_user.web_push_auth
        selected_app_user.web_push_p256dh = request.json.get('web_push_p256dh') \
            if 'web_push_p256dh' in request.json else selected_app_user.web_push_p256dh
        selected_app_user.language = request.json.get('language') \
            if 'language' in request.json else selected_app_user.language
        selected_app_user.notification_groups = (str(request.json.get('notification_groups'))
                                                 .replace('[', '').replace(']', '')
                                                 .replace('"', '')) \
            if 'notification_groups' in request.json else selected_app.notification_groups
        db_session.commit()

        json = selected_app_user.to_json()
        db_session.close()

        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


# register app user value
@sdk.route('/value/<app_hash>/<app_user_hash>', methods=['POST'])
def register_value(app_hash, app_user_hash):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.hash == app_hash).first()

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
                .filter(AppUserKey.app_id == selected_app.id, AppUserKey.key == key)\
                .first()

            if app_user_key is None:
                app_user_key = AppUserKey()
                app_user_key.app_id = selected_app.id
                app_user_key.key = key
                db_session.add(app_user_key)
                db_session.commit()

            app_user_value = db_session.query(AppUserValue)\
                .filter(AppUserValue.app_user_id == app_user.id, AppUserValue.key == key)\
                .first()

            if app_user_value is not None:
                if app_user_value.value == value:
                    db_session.close()
                    return jsonify({'message': 'Ok'}), 200

            app_user_value = AppUserValue()
            app_user_value.app_user_id = app_user.id
            app_user_value.key = key
            app_user_value.value = value
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


# register event to possibly start notification flow
@sdk.route('/event/<app_hash>/<app_user_hash>', methods=['POST'])
def register_event(app_hash, app_user_hash):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.hash == app_hash).first()

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
                .filter(Flow.app_id == selected_app.id, Flow.event == event)\
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


@sdk.route('/notifications/<notification_hash>', methods=['PUT'])
def update_notification(notification_hash):
    from magicpush.database import db_session
    try:
        app_user_notification = db_session.query(AppUserNotification)\
            .filter(AppUserNotification.hash == notification_hash)\
            .first()

        if app_user_notification is None:
            db_session.close()
            return jsonify({'message': 'Notification not found'}), 404

        if 'delivered' in request.json and request.json.get('delivered') is not None:
            if request.json.get('delivered') != app_user_notification.delivered:
                app_user_notification.delivered_at = datetime.datetime.utcnow()

            app_user_notification.delivered = request.json.get('delivered')

        if 'clicked' in request.json and request.json.get('clicked') is not None:
            if request.json.get('clicked') != app_user_notification.clicked:
                app_user_notification.clicked_at = datetime.datetime.utcnow()

            app_user_notification.clicked = request.json.get('clicked')

        db_session.commit()
        db_session.close()
        return jsonify({'message': 'Ok'}), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500
