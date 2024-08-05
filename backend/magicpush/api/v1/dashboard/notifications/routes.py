from magicpush import app
from . import notifications
from magicpush.helpers.cloudflare import Cloudflare
from magicpush.celery_tasks import send_push, schedule_notifications
from magicpush.models import App, Notification, NotificationTranslation

import datetime
from flask import jsonify, request
from flask_login import login_required, current_user


cloudflare = Cloudflare()

@notifications.route('/<app_id>', methods=['GET'])
@login_required
def get_notifications(app_id):
    from magicpush.database import db_session
    try:
        if current_user.is_admin:
            current_app = db_session.query(App).filter(App.id == app_id).first()
        else:
            current_app = db_session.query(App).filter(App.id == app_id, App.user_id == current_user.id).first()

        if current_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        page = int(request.args.get('page', 1))

        # get paged notifications
        notifications_query = Notification.query\
                         .filter(Notification.app_id == current_app.id, Notification.scheduled_at == None)\
                         .order_by(Notification.created_at.desc())\
                         .paginate(page=page, per_page=10)

        notification_list = []
        for notification in notifications_query.items:
            notification_list.append(notification.to_json())

        json = {
            'notifications': notification_list,
            'total': notifications_query.total,
        }

        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@notifications.route('/<app_id>', methods=['POST'])
@login_required
def create_notification(app_id):
    from magicpush.database import db_session
    try:
        if current_user.is_admin:
            current_app = db_session.query(App).filter(App.id == app_id).first()
        else:
            current_app = db_session.query(App).filter(App.id == app_id, App.user_id == current_user.id).first()

        if current_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        if 'name' in request.json and 'translations' in request.json:
            new_notification = Notification()
            new_notification.app_id = current_app.id
            new_notification.name = request.json.get('name')
            new_notification.scheduled_at = request.json.get('scheduled_at') \
                if 'scheduled_at' in request.json else None
            new_notification.repeat = request.json.get('repeat') \
                if 'repeat' in request.json else False
            new_notification.repeat_interval = request.json.get('repeat_interval') \
                if 'repeat_interval' in request.json else None
            new_notification.live = request.json.get('live') \
                if 'live' in request.json else False
            new_notification.sent = request.json.get('sent') \
                if 'sent' in request.json else False
            new_notification.action = request.json.get('action') \
                if 'action' in request.json else None
            db_session.add(new_notification)
            db_session.commit()

            for translation in request.json.get('translations'):
                if translation.get('language') == 'en':
                    new_notification.default_title = translation.get('title')
                    new_notification.default_message = translation.get('message')
                    new_notification.image = translation.get('image') \
                        if 'image' in translation else None
                else:
                    new_notification_translation = NotificationTranslation()
                    new_notification_translation.notification_id = new_notification.id
                    new_notification_translation.language = translation.get('language')
                    new_notification_translation.title = translation.get('title')
                    new_notification_translation.message = translation.get('message')
                    new_notification_translation.image = translation.get('image') \
                        if 'image' in translation else None
                    db_session.add(new_notification_translation)
                db_session.commit()

            if new_notification.sent is True:
                send_push.delay(new_notification.id)

            if new_notification.repeat is True:
                schedule_notifications.delay()

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


@notifications.route('<app_id>/<notification_id>', methods=['PUT'])
@login_required
def update_notification(app_id, notification_id):
    from magicpush.database import db_session
    try:
        if current_user.is_admin:
            current_app = db_session.query(App).filter(App.id == app_id).first()
        else:
            current_app = db_session.query(App).filter(App.id == app_id, App.user_id == current_user.id).first()

        if current_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        selected_notification = db_session.query(Notification)\
            .filter(Notification.id == notification_id,
                    Notification.app_id == app_id)\
            .first()

        if selected_notification is None:
            db_session.close()
            return jsonify({'message': 'Notification not found'}), 404

        if selected_notification.delivered is True:
            db_session.close()
            return jsonify({'message': 'Notification already delivered'}), 400

        if selected_notification.scheduled_at is not None and \
                datetime.datetime.utcnow() > selected_notification.scheduled_at:
            db_session.close()
            return jsonify({'message': 'Notification already delivered'}), 400

        selected_notification.name = request.json.get('name') \
            if 'name' in request.json else selected_notification.name
        selected_notification.image = request.json.get('image') \
            if 'image' in request.json else selected_notification.image
        selected_notification.scheduled_at = request.json.get('scheduled_at') \
            if 'scheduled_at' in request.json else selected_notification.scheduled_at
        selected_notification.repeat = request.json.get('repeat') \
            if 'repeat' in request.json else selected_notification.repeat
        selected_notification.repeat_interval = request.json.get('repeat_interval') \
            if 'repeat_interval' in request.json else selected_notification.repeat_interval
        selected_notification.sent = request.json.get('sent') \
            if 'sent' in request.json else selected_notification.sent
        selected_notification.live = request.json.get('live') \
            if 'live' in request.json else selected_notification.live
        selected_notification.action = request.json.get('action') \
            if 'action' in request.json else selected_notification.action

        for translation in request.json.get('translations'):
            if translation.get('language') == 'en':
                selected_notification.default_title = translation.get('title')
                selected_notification.default_message = translation.get('message')
                selected_notification.image = translation.get('image') \
                    if 'image' in translation else selected_notification.image
            else:
                notification_translation = db_session.query(NotificationTranslation)\
                    .filter(NotificationTranslation.notification_id == selected_notification.id,
                            NotificationTranslation.language == translation.get('language'))\
                    .first()
                if notification_translation is not None:
                    notification_translation.title = translation.get('title')
                    notification_translation.message = translation.get('message')
                else:
                    notification_translation = NotificationTranslation()
                    notification_translation.notification_id = selected_notification.id
                    notification_translation.language = translation.get('language')
                    notification_translation.title = translation.get('title')
                    notification_translation.message = translation.get('message')
                    db_session.add(notification_translation)
            db_session.commit()

        if selected_notification.sent is True:
            send_push.delay(selected_notification.id)

        if selected_notification.repeat is True:
            schedule_notifications.delay()

        db_session.commit()
        db_session.close()
        return jsonify({'message': 'Ok'}), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@notifications.route('<app_id>/image', methods=['POST'])
@login_required
def upload_image(app_id):
    from magicpush.database import db_session
    try:
        if current_user.is_admin:
            current_app = db_session.query(App).filter(App.id == app_id).first()
        else:
            current_app = db_session.query(App).filter(App.id == app_id, App.user_id == current_user.id).first()

        if current_app is None:
            db_session.close()
            return jsonify({'message': 'App not found'}), 404

        if 'files' in request.files:
            for image in request.files.getlist('files'):
                cloudflare_upload = cloudflare.upload()
                if cloudflare_upload is False:
                    db_session.close()
                    return jsonify({'message': 'An error occurred'}), 500

                cloudflare_file_upload = cloudflare.upload_file(cloudflare_upload['result']['uploadURL'], image)
                if cloudflare_file_upload is False:
                    db_session.close()
                    return jsonify({'message': 'An error occurred'}), 500

                image_id = cloudflare_file_upload['result']['id']

                db_session.close()
                return jsonify({'id': image_id}), 200
        else:
            db_session.close()
            return jsonify({'message': 'Data is missing'}), 400
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500
