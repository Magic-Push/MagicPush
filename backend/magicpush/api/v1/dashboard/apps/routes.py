from . import apps
from magicpush import app
from magicpush.models import App, AppUserKey, AppEvent

import os
import jwt
import datetime
from pathlib import Path
from flask import jsonify, request
from flask_login import login_required, current_user


# endpoint to get all apps
@apps.route('', methods=['GET'])
@login_required
def get_apps():
    from magicpush.database import db_session
    try:
        if current_user.is_admin:
            apps = db_session.query(App).filter(App.deleted == False).order_by(App.id.asc()).all()
        else:
            apps = db_session.query(App)\
                .filter(App.user_id == current_user.id, App.deleted == False)\
                .order_by(App.id.asc())\
                .all()

        for selected_app in apps:
            if selected_app.api_key is None:
                random_str = str(datetime.datetime.utcnow())
                encoded = jwt.encode({'id': selected_app.id, 'random': random_str}, os.getenv('RSA_PRIVATE_KEY'), algorithm='RS256')
                selected_app.api_key = encoded
                db_session.commit()

        json = {
            'apps': [added_app.to_json() for added_app in apps]
        }

        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@login_required
@apps.route('/<app_id>', methods=['GET'])
def get_app(app_id):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.id == app_id).first()

        if selected_app is None:
            db_session.close()
            return jsonify({'message': 'Not found'}), 404

        json = selected_app.to_json()

        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


# endpoint to add app
@apps.route('', methods=['POST'])
@login_required
def add_app():
    from magicpush.database import db_session
    try:
        if 'name' in request.json:
            new_app = App()
            new_app.user_id = current_user.id
            new_app.name = request.json.get('name')
            new_app.has_web = request.json.get('has_web', False)
            new_app.has_ios = request.json.get('has_ios', False)
            new_app.has_android = request.json.get('has_android', False)
            db_session.add(new_app)
            db_session.commit()

            json = new_app.to_json()

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


# endpoint to update app
@apps.route('/<app_id>', methods=['PUT'])
@login_required
def update_app(app_id):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.id == app_id).first()

        if selected_app is None:
            db_session.close()
            return jsonify({'message': 'Not found'}), 404

        if 'name' in request.json:
            selected_app.name = request.json.get('name')
        if 'apple_key_id' in request.json:
            selected_app.apple_key_id = request.json.get('apple_key_id')
        if 'apple_team_id' in request.json:
            selected_app.apple_team_id = request.json.get('apple_team_id')
        if 'apple_bundle_id' in request.json:
            selected_app.apple_bundle_id = request.json.get('apple_bundle_id')
        if 'languages' in request.json:
            selected_app.set_languages(request.json.get('languages'))
        if 'widget_color' in request.json:
            selected_app.widget_color = request.json.get('widget_color')
        if 'website_url' in request.json:
            selected_app.website_url = request.json.get('website_url')

        if 'keys' in request.json:
            existing_keys = []

            keys = db_session.query(AppUserKey).filter(AppUserKey.app_id == selected_app.id).all()
            for key in keys:
                existing_keys.append(key)

            for key in request.json.get('keys'):
                app_user_key = db_session.query(AppUserKey).filter(AppUserKey.key == key).first()
                if app_user_key is not None:
                    if app_user_key in existing_keys:
                        existing_keys.remove(app_user_key)
                else:
                    app_user_key = AppUserKey()
                    app_user_key.app_id = selected_app.id
                    app_user_key.key = key
                    db_session.add(app_user_key)

            for key in existing_keys:
                db_session.delete(key)

        if 'events' in request.json:
            existing_events = []

            events = db_session.query(AppEvent).filter(AppEvent.app_id == selected_app.id).all()
            for event in events:
                existing_events.append(event)

            for event in request.json.get('events'):
                app_event = db_session.query(AppEvent).filter(AppEvent.name == event.get('name')).first()
                if app_event is not None:
                    if app_event in existing_events:
                        existing_events.remove(app_event)
                else:
                    app_event = AppEvent()
                    app_event.app_id = selected_app.id
                    app_event.name = event
                    db_session.add(app_event)

            for event in existing_events:
                db_session.delete(event)

        db_session.commit()

        json = selected_app.to_json()

        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@apps.route('/<app_id>/generate-token', methods=['POST'])
@login_required
def generate_token(app_id):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.id == app_id).first()

        if selected_app is None:
            db_session.close()
            return jsonify({'message': 'Not found'}), 404

        random_str = str(datetime.datetime.utcnow())
        encoded = jwt.encode({'id': selected_app.id, 'random': random_str}, os.getenv('RSA_PRIVATE_KEY'), algorithm='RS256')

        db_session.close()
        return jsonify({'token': encoded}), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


# upload firebase service account file
@apps.route('/<app_id>/firebase', methods=['POST'])
@login_required
def upload_firebase_service_account_file(app_id):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.id == app_id).first()

        if selected_app is None:
            db_session.close()
            return jsonify({'message': 'Not found'}), 404

        dir = os.path.dirname(__file__)
        storage_dir = Path(dir, '../../../../storage/public/')

        if 'files' in request.files:
            file = request.files['files']
            file.save(Path(storage_dir, file.filename))
            selected_app.firebase_service_account_file = file.filename
            db_session.commit()
            db_session.close()
            return jsonify({'id': file.filename}), 200
        else:
            db_session.close()
            return jsonify({'message': 'Data is missing'}), 400
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


# upload apple key file
@apps.route('/<app_id>/apple', methods=['POST'])
@login_required
def upload_apple_key_file(app_id):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.id == app_id).first()

        if selected_app is None:
            db_session.close()
            return jsonify({'message': 'Not found'}), 404

        dir = os.path.dirname(__file__)
        storage_dir = Path(dir, '../../../../storage/public/')

        if 'files' in request.files:
            file = request.files['files']
            file.save(Path(storage_dir, file.filename))
            selected_app.apple_key_file = file.filename
            db_session.commit()
            db_session.close()
            return jsonify({'id': file.filename}), 200
        else:
            db_session.close()
            return jsonify({'message': 'Data is missing'}), 400
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


# endpoint to delete app
@apps.route('/<app_id>', methods=['DELETE'])
@login_required
def delete_app(app_id):
    from magicpush.database import db_session
    try:
        selected_app = db_session.query(App).filter(App.id == app_id).first()

        if selected_app is None:
            db_session.close()
            return jsonify({'message': 'Not found'}), 404

        selected_app.deleted = True
        selected_app.deleted_at = datetime.datetime.utcnow()
        db_session.commit()
        db_session.close()
        return jsonify({'message': 'Ok'}), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500
