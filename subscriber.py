from globals import INBOUND_CHANNEL
from connector import connect_to_redis_server

def create_subscriber():
	"""
	This function creates a set Redis client
	which is subscribed to the INBOUND_CHANNEL.
	This client will be used in order to receive
	all messages sent from the Vue.js web app.
	"""
	client = connect_to_redis_server()
	sub = client.pubsub()
	sub.subscribe(INBOUND_CHANNEL)
	return sub

def handle_message(message):
	"""
	This function handles messsages which have been
	sent from the Vue.js web app, and prints out the
	message for logging purposes.
	Please note, that it must be used in every occasion
	when a Redis client is subscribed.
	"""
	if message and not message['data'] == 1:
			message = message['data'].decode('utf-8')
			platform, action, details = message.split(':')
			print 'Received command: {}'.format(message)
			# print 'Action: %s on platform: %s' % (action, platform, details)
			return platform, action, details

if __name__ == '__main__':
	"""
	You can run this file as a seperate Python file, if you'd
	like to run a subscribed Redis client.
	"""
	sub = create_subscriber()
	while True:
		platform, action, details = "", "", ""
		try:
			platform, action, details = handle_message(sub.get_message())
			print (platform, action, details)
		except:
			pass
