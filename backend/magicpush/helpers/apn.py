from magicpush import app

import os
import jwt
import time
import json
import requests
from pathlib import Path
from hyper import HTTPConnection, HTTP20Connection


class Apn(object):

    def send(self, selected_app, app_user, notification_hash, notification):
        dir = os.path.dirname(__file__)
        path = Path(dir, '../storage/public/{}'.format(selected_app.apple_key_file))

        p8_file = open(str(path), 'r')
        secret = p8_file.read()
        token = jwt.encode({
                'iss': selected_app.apple_team_id,
                'iat': time.time()
            },
            secret,
            algorithm='ES256',
            headers={
                'alg': 'ES256',
                'kid': selected_app.apple_key_id,
            }
        )

        endpoint = '/3/device/{}'.format(app_user.apn_device_token)

        headers = {
            'apns-expiration': '0',
            'apns-priority': '10',
            'apns-push-type': 'alert',
            'apns-topic': selected_app.apple_bundle_id,
            'apns-collapse-id': notification_hash,
            'authorization': 'bearer {}'.format(token)
        }
        print(headers)

        payload_data = {
            'aps': {
                'alert': {
                    'title': notification.default_title,
                    'body': notification.default_message
                },
                'mutable-content': 1,
                'sound': 'default'
            }
        }

        conn = HTTP20Connection(app.config.get('APN_HOST'), force_proto='h2')

        payload = json.dumps(payload_data).encode('utf-8')

        conn.request(
            'POST',
            endpoint,
            payload,
            headers=headers
        )

        response = conn.get_response()

        if response.status == 200:
            print('APN Success: {}'.format(response.read()))
            return True
        else:
            app.logger.exception('App: {} APN Error: {}'.format(selected_app.id, response.read()))
            return False
