import os
import jwt
import datetime
from pathlib import Path
from flask import jsonify

from magicpush.models import User
from magicpush import login_manager, db


@login_manager.request_loader
def load_user_from_request(request):
    if 'Authorization' in request.headers:
        token = request.headers.get('Authorization')
        if token is not None and 'Bearer' in token:
            print('Token ' + token)
            try:
                token = token[token.index('Bearer') + 7:]

                dir = os.path.dirname(__file__)
                public_key = Path(dir, '../../../storage/private/id_rsa.pub')
                with open(public_key) as f:
                    decoded = jwt.decode(token, f.read(), algorithms='RS256')

                if 'type' not in decoded or decoded['type'] != 'auth':
                    return None

                user = User.query.filter_by(id=decoded['id']).first()

                user.last_active_at = datetime.datetime.utcnow()
                db.session.commit()

                return user
            except jwt.exceptions.ExpiredSignatureError as e:
                print('Expired')
                return None
            except jwt.exceptions.InvalidTokenError as e:
                print('Invalid')
                return None
    return None


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return jsonify({'message': 'Unauthorized'}), 401
