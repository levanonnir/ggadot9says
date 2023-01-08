from connector import connect_to_redis_server

env = 'ggadot'

client = connect_to_redis_server()

p = client.pubsub()
p.subscribe(env)

while True:
	message = p.get_message()

	if message and not message['data'] == 1:
		message = message['data'].decode('utf-8')
		action, platform = message.split('::')
		print 'Received command: {}'.format(message)
		print 'Action: %s on platform: %s' % (action, platform)