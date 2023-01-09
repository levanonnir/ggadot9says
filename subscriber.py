from globals import CHANNEL
from connector import connect_to_redis_server

def create_subscriber():
	client = connect_to_redis_server()
	sub = client.pubsub()
	sub.subscribe(CHANNEL)
	return sub

def handle_message(message):
	if message and not message['data'] == 1:
			message = message['data'].decode('utf-8')
			platform, action, details = message.split(':')
			print 'Received command: {}'.format(message)
			print 'Action: %s on platform: %s' % (action, platform, details)
			return platform, action, details