import os

import requests

from magicpush import app


class Mailgun(object):

    host = 'https://api.eu.mailgun.net/v3/{}/'.format(os.getenv('MAILGUN_DOMAIN'))

    def send(self, to, subject, body):
        url = self.host + 'messages'

        data = {
            'from': 'MagicPush <{}>'.format(os.getenv('MAILGUN_FROM')),
            'to': to,
            'subject': subject,
            'html': body
        }

        response = requests.post(url, auth=('api', os.getenv('MAILGUN_API_KEY')), data=data)

        if response.status_code is 200:
            app.logger.info('Send email: ' + str(response.status_code) + ' : ' + response.text)
            return True
        else:
            app.logger.exception('Error sending email: ' + str(response.status_code) + ' : ' + response.text)
            return False
