import os
import requests

from magicpush import app


class Cloudflare(object):

    host = 'https://api.cloudflare.com/client/v4/'

    def upload(self):
        url = self.host + 'accounts/{}/images/v2/direct_upload'.format(app.config.get('CLOUDFLARE_ACCOUNT_ID'))

        headers = {
            'Authorization': 'Bearer ' + app.config.get('CLOUDFLARE_ACCESS_TOKEN'),
        }

        payload = {
            'requireSignedURLs': (None, True)
        }

        response = requests.post(url, headers=headers, files=payload)
        print(response.text)
        if response.status_code == 200:
            return response.json()
        else:
            app.logger.exception('Cloudflare upload ' + str(response.status_code) + ': ' + response.text)
            return False

    def upload_file(self, url, file):
        payload = {
            'file': file
        }

        response = requests.post(url, files=payload)
        print(response.text)
        if response.status_code == 200:
            return response.json()
        else:
            app.logger.exception('Cloudflare upload file ' + str(response.status_code) + ': ' + response.text)
            return False
