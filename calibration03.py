from scorpy.simpleView import calibration
from scorpy.scorbotAPI import Client
from savePic import savePic
from contours import Contour

# Start by calibrating the robot:
robot = Client()
calibrator = calibration.Translator2D()

p1 = (188, 316) # Blue
p2 = (234, 144) # Yellow
p3 = (423, 244) # Green

q1 = robot.get_position_coordinates(1) # Green
q2 = robot.get_position_coordinates(2) # Blue
q3 = robot.get_position_coordinates(3) # Yellow

calibrator.calibration(p1, p2, p3, q1, q2, q3)

robot.teach_relative_xyz_position(10, 0, 0, 50, 0, 0, 1)

robot.move(99, 80)
robot.close_gripper()

# Continue with taking the picture:
image_path = 'new_image.jpg'
savePic(image_path, flag=1)

# Crop the red box:

objects_number = 3
cont = Contour(image_path, objects_number)
cont.show()
cms = cont.get_cm()
angles = cont.get_angles()
for i in range(objects_number):
    p4 = cms[i]
    q4 = calibrator.transform_point(p4)
    angle = angles[i] if angles[i] < 180 else 180 - angles[i]
    height_df = 20 * i
    drop_off_position = 10 + i
    robot.teach_absolute_xyz_position(40, q4[0], q4[1], q1[2]+50+height_df, q1[3], angle)
    robot.teach_relative_xyz_position(4, 0, 0, -50-height_df, 0, 0, 40)
    robot.teach_relative_xyz_position(drop_off_position, 0, 0, q1[2] + height_df, 0, 0, 1)
    robot.teach_relative_xyz_position(98, 0, 0, 50 + q1[2] + height_df, 0, 0, 1)
    # Go to target:
    robot.open_gripper()
    robot.move_linear(40)
    robot.move_linear(4)
    robot.close_gripper()
    robot.move_linear(40)
    # Go to drop off:
    robot.move_linear(98)
    robot.move_linear(drop_off_position)
    robot.open_gripper()
    robot.move_linear(98)