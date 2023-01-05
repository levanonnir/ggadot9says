import sys
from connector import connect_to_redis_server

if len(sys.argv) == 3:
	program, environment, action = sys.argv

	client = connect_to_redis_server()

	client.publish(environment, action)
else:
	print('You must give an environment, and an action!')