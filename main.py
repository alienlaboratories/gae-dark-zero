#
# Copyright 2015 Alien Laboratories, Inc.
#

import os
import flask
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3 import Retry


__version__ = '0.0.1'

# TODO(burdon): Config.
FRONTEND_SERVER = 'http://www.darkzero.net'
PUSH_URL = os.path.join(FRONTEND_SERVER, 'webhook/google/push/email')


logging.basicConfig()
LOG = logging.getLogger(__name__)


# Flask instance.
app = flask.Flask(__name__)


# TODO(burdon): Use memcache since reset on each invocation.
STATS = {
    'sent': 0,
    'errors': 0
}


@app.route('/')
def home():
    return flask.jsonify({
        'module': 'Dark Zero',
        'version': __version__,
        'server': PUSH_URL,
        'stats': STATS
    })


@app.route('/push/email', methods=['POST'])
def push_email():
    """Receives Google API push notification and relays to frontend.
    GAE supports HTTPS automatically, so we use it as a proxy."""

    # https://developers.google.com/gmail/api/guides/push
    LOG.info('Push: %s' % flask.request.json)

    with requests.Session() as session:

        # noinspection PyTypeChecker
        session.mount('http://', HTTPAdapter(max_retries=Retry(total=5, backoff_factor=.5)))

        # Content.
        data = flask.request.data

        # Make request.
        r = session.post(PUSH_URL, data=data)
        if r.status_code == requests.codes.ok:
            STATS['sent'] += 1
            LOG.info('Posted notification.')
        else:
            STATS['errors'] += 1
            r.raise_for_status()

    return flask.make_response()


#
# https://appengine.google.com/dashboard?&app_id=s~dark-zero
#
if __name__ == '__main__':
    app.run()
