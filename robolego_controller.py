from robolego import Lego
from subscriber import create_subscriber, handle_message
from connector import connect_to_redis_server
from globals import CHANNEL

if __name__ == "__main__":
  sub = create_subscriber()
  pub = connect_to_redis_server()
  lego = Lego()
  robolego_connected = False
  power = 30
  robolego_name = ""

  while True:
    platform, action, details = handle_message(sub.get_message())
    
    if robolego_connected and platform == robolego_name:
      # Execute command only if the robot is connected, and the command was sent to him.
      if action == 'sample_color':
        pub.publish(CHANNEL, "%s:status:sampling" % robolego_name)
        color = lego.sample_color()
        pub.publish(CHANNEL, "%s:color:%s" % (robolego_name, color))
        pub.publish(CHANNEL, "%s:status:online" % robolego_name)
      elif "power" in action:
        power = details
        print "%s's power changed to %s" % (platform, power)
      elif action in lego.movementDirections:
        movement_function = getattr(lego, action)
        movement_function(power)
        if action != "stop":
          pub.publish(CHANNEL, "%s:status:moving" % robolego_name)
        else:
          pub.publish(CHANNEL, "%s:status:online" % robolego_name)
    else:
      if platform == 'lego' and action == 'connect':
        message = "%s:status:" % details
        try:
          lego.connect(details)
          robolego_name = details
          robolego_connected = True
          pub.publish(CHANNEL, message + "online")
        except Exception as e:
          print "Error while attempting to connect to %s: %s" % (details, e)
          pub.publish(CHANNEL, message + "offline")

