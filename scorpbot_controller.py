from scorpbot import ScorpBot
from subscriber import create_subscriber, handle_message
from connector import connect_to_redis_server
from globals import OUTBOUND_CHANNEL, COLORS

if __name__ == "__main__":
  sub = create_subscriber()
  pub = connect_to_redis_server()
  scorp = ScorpBot()
  scorpbot_connected = False
  print "ScorpBot awaiting orders..."
  while True:
    platform, action, details = "", "", ""
    try:
      platform, action, details = handle_message(sub.get_message())
    except:
      pass

    if platform == 'scorp':
      message = "%s:status:" % platform
      if scorpbot_connected:
        if action == "action" and details == 'home':
          print "Publish: %shoming" % message
          pub.publish(OUTBOUND_CHANNEL, message + "homing")
          scorp.go_home()
          print "Publish: %sonline" % message
          pub.publish(OUTBOUND_CHANNEL, message + "online")
        elif action == "action" and details == "calibrate":
          print "Publish: %scalibrating" % message
          pub.publish(OUTBOUND_CHANNEL, message + "calibrating")
          scorp.calibrate()
          print "Publish: %sonline" % message
          pub.publish(OUTBOUND_CHANNEL, message + "online")
        # elif details == ""
        elif action == "action" and "move" in details:
          _, point = details.split("_")
          print "Publish: %smoving" % message
          pub.publish(OUTBOUND_CHANNEL, message + "moving")
          scorp.move(point)
          print "Publish: %sonline" % message
          pub.publish(OUTBOUND_CHANNEL, message + "online")
        elif details in COLORS.values():
          print "Publish: %smoving to %s" % (message, details)
          pub.publish(OUTBOUND_CHANNEL, message + "moving to %s" % details)
          scorp.touch_color_point(details)
          print "Publish: %sonline" % message
          pub.publish(OUTBOUND_CHANNEL, message + "online")

      else:
        if details == 'connect':
          try:
            print "Publish: %shoming" % message
            pub.publish(OUTBOUND_CHANNEL, message + "homing")
            # scorp.go_home()
            print "Publish: %scalibrating" % message
            pub.publish(OUTBOUND_CHANNEL, message + "calibrating")
            scorp.calibrate()
            print "Publish: %sonline" % message
            pub.publish(OUTBOUND_CHANNEL, message + "online")
            scorpbot_connected = True
          except Exception as e:
            print "Error while attempting to connect to %s: %s" % (platform, e)
            print "Publish: %soffline" % message
            pub.publish(OUTBOUND_CHANNEL, message + "offline")