#
# Copyright 2015 Alien Laboratories, Inc.
#

from apiclient import discovery
from oauth2client.client import GoogleCredentials
import flask
import httplib2
import logging


LOG = logging.getLogger(__name__)


# TODO(burdon): Just mirror notifications to frontend.

PUBSUB_SCOPES = ['https://www.googleapis.com/auth/pubsub']

PROJECT = 'dark-zero'

TOPIC = 'projects/{project}/topics/email'.format(project=PROJECT)

SUBSCRIPTION = 'projects/{project}/subscriptions/email'.format(project=PROJECT)

SERVER_NAME = 'www.dark-zero.net'


# https://cloud.google.com/pubsub/configure
def create_pubsub_client(http=None):
    if not http:
        http = httplib2.Http()
    credentials = GoogleCredentials.get_application_default()
    if credentials.create_scoped_required():
        credentials = credentials.create_scoped(PUBSUB_SCOPES)
    credentials.authorize(http)
    return discovery.build('pubsub', 'v1', http=http)


# Flask instance.
app = flask.Flask(__name__)


@app.route('/')
def home():
    return 'Dark Zero'


@app.route('/notify', methods=['POST'])
def notify():
    # https://developers.google.com/gmail/api/guides/push
    LOG.info('Notification: %s' % flask.request.json)
    return flask.make_response()


# TODO(burdon): Move to frontend project.
@app.route('/init')
def init():
    # Gmail Push Notifications.
    # MASTER DOC: https://developers.google.com/gmail/api/guides/push

    # 1. Set-up PubSub client
    # https://cloud.google.com/pubsub/configure
    client = create_pubsub_client()

    # 2. Create topic.
    # https://cloud.google.com/pubsub/publisher#create
    try:
        LOG.info('Creating topic...')
        topic = client.projects().topics().create(name=TOPIC, body={}).execute()
        LOG.info('Created topic: %s' % topic.get('name'))

    except Exception as ex:
        LOG.exception(ex)

    # 3. Create subscription.
    # https://cloud.google.com/pubsub/subscriber
    # TODO(burdon): User url_for (absolute). Set SERVER_NAME.
    body = {
        'topic': TOPIC,
        'pushConfig': {
            'pushEndpoint': 'https://{server}/notify'.format(server=SERVER_NAME)
        }
    }
    print 'https://{server}/notify'.format(server=SERVER_NAME)

    try:
        LOG.info('Creating subscription...')
        subscription = client.projects().subscriptions().create(name=SUBSCRIPTION, body=body).execute()
        LOG.info('Created: %s' % subscription.get('name'))

    except Exception as ex:
        LOG.exception(ex)

    # 4. Grant publish rights.
    # https://developers.google.com/gmail/api/guides/push
    policy = {
      'policy': {
        'bindings': [{
          'role': 'roles/pubsub.publisher',
          'members': ['serviceAccount:gmail-api-push@system.gserviceaccount.com'],
        }],
      }
    }

    response = None
    try:
        LOG.info('Granting rights...')
        response = client.projects().topics().setIamPolicy(resource=TOPIC, body=policy).execute()
        LOG.info('OK: %s' % response)

    except Exception as ex:
        LOG.exception(ex)

    # TODO(burdon): Do this from frontend.
    # TODO(burdon): Renew every 7 days.
    # 5. Get email updates.
    # https://developers.google.com/gmail/api/guides/push
    # gmail = create_gmail_client()
    #
    # request = {
    #     'labelIds': ['INBOX'],
    #     'topicName': TOPIC
    # }
    #
    # try:
    #     # TODO(burdon): Config users.
    #     LOG.info('Get updates...')
    #     response = gmail.users().watch(userId='me', body=request).execute()
    #     print response
    #
    # except Exception as ex:
    #     LOG.error(ex)

    return flask.jsonify(response)


if __name__ == '__main__':
    app.run()
