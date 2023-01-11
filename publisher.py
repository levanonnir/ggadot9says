"""
This file can be run in order to publish a message to the Redis AWS server.
In order to do this, run:
python publisher.py _channel_ _message_
"""

import sys
from connector import connect_to_redis_server

if len(sys.argv) == 3:
	program, environment, action = sys.argv

	client = connect_to_redis_server()

	client.publish(environment, action)
else:
	print('You must give an environment, and an action!')