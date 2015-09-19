#
# Copyright 2015 Alien Laboratories, Inc.
#

from apiclient import discovery
from oauth2client.client import GoogleCredentials
import flask
import httplib2
import logging


# TODO(burdon): Config.
FRONTEND_SERVER = 'http://www.dark-zero.net'
PUSH_URL = os.path.join(FRONTEND_SERVER, '/webhook/google/push/email')


logging.basicConfig()
LOG = logging.getLogger(__name__)


# Flask instance.
app = flask.Flask(__name__)


@app.route('/')
def home():
    return 'Dark Zero'


@app.route('/push/email', methods=['POST'])
def push_email():
    """Receives Google API push notification and relays to frontend.
    GAE supports HTTPS automatically, so we use it as a proxy."""

    # https://developers.google.com/gmail/api/guides/push
    LOG.info('Notification: %s' % flask.request.json)

    with requests.Session() as session:

        # noinspection PyTypeChecker
        session.mount('http://', HTTPAdapter(max_retries=Retry(total=5, backoff_factor=.5)))

        # Content.
        data = flask.request.data

        # Make request.
        r = session.post(PUSH_URL, data=data)
        if r.status_code == requests.codes.ok:
            LOG.info('Posted notification.')
        else:
            r.raise_for_status()

    return flask.make_response()

#
# https://appengine.google.com/dashboard?&app_id=s~dark-zero
#
if __name__ == '__main__':
    app.run()
