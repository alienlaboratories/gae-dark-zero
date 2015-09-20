#
# Copyright 2015 Alien Laboratories, Inc.
#

import os
import flask
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3 import Retry
from google.appengine.api import memcache


# TODO(burdon): Link to GAE version.
__version__ = '0.0.2'


# TODO(burdon): Config.
# TODO(burdon): Create /webhook/{hook} Generated and mapped to different hooks.
FRONTEND_SERVER = 'http://darkzero.net'
PUSH_URL = os.path.join(FRONTEND_SERVER, 'webhook/google/push/email')


# Memcache
KEY_ERROR = 'push.error'
KEY_SENT = 'push.sent'


logging.basicConfig()
LOG = logging.getLogger(__name__)


# Flask instance.
app = flask.Flask(__name__)


@app.route('/')
def home():
    return flask.jsonify({
        'module': 'Dark Zero',
        'version': __version__,
        'server': PUSH_URL,
        'stats': {
            KEY_SENT: memcache.get(KEY_SENT) or 0,
            KEY_ERROR: memcache.get(KEY_ERROR) or 0
        }
    })


@app.route('/push/email', methods=['POST'])
def push_email():
    """Receives Google API push notification and relays to frontend.
    GAE supports HTTPS automatically, so we use it as a proxy."""

    # https://developers.google.com/gmail/api/guides/push
    # Test: curl -X POST http://www.darkzero.net/webhook/google/push/email
    with requests.Session() as session:

        # noinspection PyTypeChecker
        session.mount('http://', HTTPAdapter(max_retries=Retry(total=5, backoff_factor=.5)))

        headers = {
            'Content-Type': 'application/json'
        }

        data = flask.request.data

        # Make request.
        r = session.post(PUSH_URL, headers=headers, data=data)
        if r.status_code == requests.codes.ok:
            memcache.incr(KEY_SENT)
            LOG.info('Pushed: %s:%s' % (PUSH_URL, flask.request.json()))
        else:
            memcache.incr(KEY_ERROR)
            r.raise_for_status()

    return flask.make_response()


#
# https://appengine.google.com/dashboard?&app_id=s~dark-zero
#
if __name__ == '__main__':
    app.run()
