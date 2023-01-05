from globals import HOST, PORT, PASSWORD
import redis

def connect_to_redis_server():
  """
  This function connects to the project's Redis server,
  and returns it as an object to be used.
  """
  try:
    r = redis.Redis(
      host=HOST,
      port=PORT,
      password=PASSWORD)
  except Exception as e:
    print "Error connecting to Redis server: %s" % e
  return r

if __name__ == '__main__':
  r = connect_to_redis_server()
  connected = r.ping()
  if connected:
    print "Successfully pinged Redis server."
  else:
    print "Failed to ping Redis server."