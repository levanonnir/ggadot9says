from scorpbot import ScorpBot
from subscriber import create_subscriber, handle_message
from connector import connect_to_redis_server
from globals import OUTBOUND_CHANNEL, COLORS

if __name__ == "__main__":
  sub = create_subscriber()
  pub = connect_to_redis_server()
  scorp = ScorpBot()
  scorpbot_connected = False
  while True:
    platform, action, details = "", "", ""
    try:
      platform, action, details = handle_message(sub.get_message())
    except:
      pass

    if scorpbot_connected:
      if action == "action" and details == 'home':
        print "Publish: %s:status:homing" % platform
        pub.publish(OUTBOUND_CHANNEL, message + "homing")
        scorp.go_home()
        print "Publish: %s:status:online" % platform
        pub.publish(OUTBOUND_CHANNEL, message + "online")
      elif action == "calibrate":

        print "Publish: %s:status:online" % platform
        pub.publish(OUTBOUND_CHANNEL, message + "online")
      # elif details == ""
      elif action == "action" and "move" in details:
        _, point = details.split("_")
        print "Publish: %s:status:moving" % platform
        pub.publish(OUTBOUND_CHANNEL, message + "moving")
        scorp.move(point)
        print "Publish: %s:status:online" % platform
        pub.publish(OUTBOUND_CHANNEL, message + "online")
      elif details in COLORS.values():



    else:
      if platform == 'scorp' and details == 'connect':
        message = "%s:status:" % platform
        try:
          print "Publish: %s:status:homing" % platform
          pub.publish(OUTBOUND_CHANNEL, message + "homing")
          scorp.go_home()
          print "Publish: %s:status:calibrating" % platform
          pub.publish(OUTBOUND_CHANNEL, message + "calibrating")
          scorp.calibrate()
          print "Publish: %s:status:online" % platform
          pub.publish(OUTBOUND_CHANNEL, message + "online")
          scorpbot_connected = True
        except Exception as e:
          print "Error while attempting to connect to %s: %s" % (platform, e)
          print "Publish: %s:status:offline" % platform
          pub.publish(OUTBOUND_CHANNEL, message + "offline")