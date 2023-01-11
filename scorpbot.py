from scorpy.scorbotAPI import Client
from scorpy.simpleView import calibration
from globals import OUTBOUND_CHANNEL, COLORS


class ScorpBot():
    def __init__(self):
        self.robot = Client()
        self.robot.close_gripper()

    def go_home(self):
        self.robot.home_robot()

    def calibrate(self):
        self.calibrator = calibration.Translator2D()
        p1 = (769, 290)
        p3 = (675, 304)
        p2 = (859, 234)
        self.robot.teach_absolute_xyz_position(1, 304, 5, 55, -107, -324)
        q1 = self.robot.get_position_coordinates(1)
        self.robot.teach_absolute_xyz_position(10, 303, 31, 59, -107, -324)
        q2 = self.robot.get_position_coordinates(10)
        self.robot.teach_absolute_xyz_position(20, 304, -14, 55, -107, -324)
        q3 = self.robot.get_position_coordinates(20)
        self.calibrator.calibration(p1, p2, p3, q1, q2, q3)


    # def teach_positions(self,num_point,x,y,z,pitch,roll):
    #     self.robot.teach_absolute_xyz_position(num_point,x,y,z,pitch,roll)
    # blue position - (1, 359, -26, 47, -107, -324)
    # red position - (2,346, 41, 50, -107, -324)
    # white position - (3, 304, 5, 55, -107, -324)
    # orange position - (4, 259, 52, 54, -107, -324)
    # green position -(5,234, 9, 56, -107, -324)

# s = ScorpBot()
# s.robot.move(20)

