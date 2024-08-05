from magicpush import app

import os
import json
import requests
from pathlib import Path
from oauth2client.service_account import ServiceAccountCredentials


class Fcm(object):

    scopes = ['https://www.googleapis.com/auth/firebase.messaging']

    def get_access_token(self, selected_app):
        dir = os.path.dirname(__file__)
        path = Path(dir, '../storage/public/{}'.format(selected_app.firebase_service_account_file))
        credentials = ServiceAccountCredentials.from_json_keyfile_name(path.absolute(), self.scopes)
        access_token_info = credentials.get_access_token()
        return access_token_info.access_token

    def get_project_id(self, selected_app):
        dir = os.path.dirname(__file__)
        path = Path(dir, '../storage/public/{}'.format(selected_app.firebase_service_account_file))
        # parse json from file
        with open(path, 'r') as file:
            data = json.load(file)
            return data['project_id']

    def send(self, selected_app, app_user, notification_hash, notification):
        endpoint = app.config.get('FCM_HOST') + 'projects/{}/messages:send'.format(self.get_project_id(selected_app))

        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + self.get_access_token(selected_app)
        }

        post_data = {
            'message': {
                'data': {
                    'hash': notification_hash,
                },
                'android': {
                    'notification': {
                        'click_action': 'magicpush.android.sdk.NOTIFICATION_CLICK'
                    }
                },
                'notification': {
                    'title': notification.default_title,
                    'body': notification.default_message,
                    'image': 'https://imagedelivery.net/MUP9cvwIiXaVOmbyPlpx4w/{}/public'.format(notification.image)
                    if notification.image is not None else None
                },
                'token': app_user.fcm_token
            }
        }

        response = requests.post(endpoint, headers=headers, json=post_data)
        if response.status_code is 200:
            app.logger.info('Send push: ' + str(response.status_code) + ' : ' + response.text)
            return True
        else:
            app.logger.exception('Error sending push: ' + str(response.status_code) + ' : ' + response.text)
            return False
