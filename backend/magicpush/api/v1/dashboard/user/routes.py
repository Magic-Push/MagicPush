import os
import jwt
import uuid
import datetime
from pathlib import Path
from sqlalchemy import or_
from flask_mail import Message
from flask import jsonify, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import users
from magicpush import app
from magicpush.helpers.mailgun import Mailgun
from magicpush.models import User, App, AppUser

mail = Mailgun()


@users.route('/early-access', methods=['POST'])
def early_access():
    from magicpush.database import db_session
    try:
        if 'email' in request.json:
            email = request.json.get('email')

            user = db_session.query(User).filter(User.email == email).first()

            if user is not None:
                db_session.close()
                return jsonify({'message': 'Email is already in use'}), 400

            user = User()
            user.email = email
            user.early_access = True
            db_session.add(user)
            db_session.commit()
            db_session.close()
            return jsonify({'message': 'Ok'}), 200
        else:
            db_session.close()
            return jsonify({'message': 'Data is missing'}), 400
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@users.route('/login', methods=['POST'])
def login():
    from magicpush.database import db_session
    try:
        if 'email' in request.json and 'password' in request.json:
            email = request.json.get('email')
            password = request.json.get('password')

            user = db_session.query(User).filter(User.email == email).first()

            if user is None:
                db_session.close()
                return jsonify({'message': 'Invalid credentials'}), 400

            if check_password_hash(user.password, password) is True:
                expires_in = datetime.datetime.utcnow() + datetime.timedelta(weeks=1)

                encoded = jwt.encode(
                    {
                        'type': 'auth',
                        'id': user.id,
                        'exp': expires_in
                    }, os.getenv('RSA_PRIVATE_KEY'), algorithm='RS256')

                json = {
                    'token': encoded,
                    'user': user.to_json()
                }
                db_session.close()
                return jsonify(json), 200
            else:
                db_session.close()
                return jsonify({'message': 'Invalid credentials'}), 400
        else:
            db_session.close()
            return jsonify({'message': 'Data is missing'}), 400
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@users.route('/signup', methods=['POST'])
def signup():
    from magicpush.database import db_session
    try:
        if 'name' in request.json and 'email' in request.json and 'password' in request.json:
            name = request.json.get('name')
            email = request.json.get('email')
            password = request.json.get('password')

            user = db_session.query(User).filter(User.email == email).first()

            if user is not None:
                db_session.close()
                return jsonify({'message': 'Email is already in use'}), 400

            user = User()
            user.name = name
            user.email = email
            user.password = generate_password_hash(password)
            db_session.add(user)
            db_session.commit()

            encoded_verify = jwt.encode(
                {
                    'type': 'verify',
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=48)
                }, os.getenv('RSA_PRIVATE_KEY'), algorithm='RS256')

            message = ("Welcome to MagicPush! <br> We are super happy to have you on board! "
                       "Please confirm your email address by going to <a href=\"{}\">{}</a>."
                       .format('https://app.getmagicpush.com/auth/verify/{}'.format(encoded_verify),
                               'https://app.getmagicpush.com/auth/verify/{}'.format(encoded_verify)))
            mail.send(user.email, 'Verify your email address', message)

            encoded = jwt.encode(
                {
                    'type': 'auth',
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=1)
                }, os.getenv('RSA_PRIVATE_KEY'), algorithm='RS256')

            json = {
                'token': encoded,
                'user': user.to_json()
            }
            db_session.close()
            return jsonify(json), 200
        else:
            db_session.close()
            return jsonify({'message': 'Data is missing'}), 400
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@users.route('', methods=['GET'])
@login_required
def get_user():
    from magicpush.database import db_session
    try:
        user = db_session.query(User).filter(User.id == current_user.id).first()

        if user is None:
            db_session.close()
            return jsonify({'message': 'Not found'}), 404

        json = user.to_json()
        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@users.route('', methods=['PUT'])
@login_required
def update_user():
    from magicpush.database import db_session
    try:
        user = db_session.query(User).filter(User.id == current_user.id).first()

        if user is None:
            db_session.close()
            return jsonify({'message': 'Not found'}), 404

        if 'email' in request.json:
            email = request.json.get('email')

            if email != user.email:
                encoded_verify = jwt.encode(
                    {
                        'type': 'change-email',
                        'id': user.id,
                        'email': email,
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
                    }, os.getenv('RSA_PRIVATE_KEY'), algorithm='RS256')

                message = ("Hello, we have received a request to change your account's email address. If that was you please click here <a href=\"{}\">{}</a>.<br> <b>If that wasn't you, change your password.</b>"
                           .format('https://app.getmagicpush.com/auth/change/{}'.format(encoded_verify),
                                   'https://app.getmagicpush.com/auth/change/{}'.format(encoded_verify)))
                mail.send(user.email, 'Email address change requested', message)

        user.name = request.json.get('name') \
            if 'name' in request.json else user.name
        user.business_name = request.json.get('business_name') \
            if 'business_name' in request.json else user.business_name
        user.country = request.json.get('country') \
            if 'country' in request.json else user.country
        user.vat_number = request.json.get('vat_number') \
            if 'vat_number' in request.json else user.vat_number
        user.website_url = request.json.get('website_url') \
            if 'website_url' in request.json else user.website_url
        db_session.commit()

        json = user.to_json()
        db_session.close()
        return jsonify(json), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@users.route('/request-reset', methods=['POST'])
def request_reset():
    from magicpush.database import db_session
    try:
        if 'email' in request.json:
            email = request.json.get('email')

            user = db_session.query(User).filter(User.email == email).first()

            if user is None:
                db_session.close()
                return jsonify({'message': 'Email not found'}), 404

            encoded = jwt.encode(
                {
                    'type': 'password-reset',
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }, os.getenv('RSA_PRIVATE_KEY'), algorithm='RS256')

            message = ("Hello, we have received a request to reset your account's password. If that was you please click <a href=\"{}\">here</a>.<br> <b>If that wasn't you, ignore this email.</b>"
                       .format('https://app.getmagicpush.com/auth/reset/{}'.format(encoded),
                               'https://app.getmagicpush.com/auth/reset/{}'.format(encoded)))
            mail.send(user.email, 'Password reset requested', message)

            db_session.close()
            return jsonify({'message': 'Ok'}), 200
        else:
            db_session.close()
            return jsonify({'message': 'Data is missing'}), 400
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


@users.route('/reset/<token>', methods=['POST'])
def reset_password(token):
    from magicpush.database import db_session
    try:
        dir = os.path.dirname(__file__)
        public_key = Path(dir, '../../../../storage/private/id_rsa.pub')
        with open(public_key) as f:
            decoded = jwt.decode(token, f.read(), algorithms='RS256')

        if decoded['type'] != 'password-reset':
            db_session.close()
            return jsonify({'message': 'Invalid token'}), 400

        user = db_session.query(User).filter(User.id == decoded['id']).first()

        if user is None:
            db_session.close()
            return jsonify({'message': 'User not found'}), 404

        user.password = generate_password_hash(request.json.get('password'))
        db_session.commit()
        db_session.close()
        return jsonify({'message': 'Ok'}), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500


# endpoint to verify user email from the generated token
@users.route('/verify/<token>', methods=['POST'])
def verify_token(token):
    from magicpush.database import db_session
    try:
        dir = os.path.dirname(__file__)
        public_key = Path(dir, '../../../../storage/private/id_rsa.pub')
        with open(public_key) as f:
            decoded = jwt.decode(token, f.read(), algorithms='RS256')

        if decoded['type'] != 'verify':
            db_session.close()
            return jsonify({'message': 'Invalid token'}), 400

        user = db_session.query(User).filter(User.id == decoded['id']).first()

        if user is None:
            db_session.close()
            return jsonify({'message': 'User not found'}), 404

        user.email_verified = True
        user.email_verified_at = datetime.datetime.utcnow()
        db_session.commit()
        db_session.close()
        return jsonify({'message': 'Ok'}), 200
    except Exception as e:
        app.logger.exception(e)
        db_session.rollback()
        db_session.expunge_all()
        db_session.close()
        return jsonify({'message': 'An error occurred'}), 500
