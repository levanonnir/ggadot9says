from scorpy.scorbotAPI import Client
from scorpy.simpleView import calibration
from webcam import Webcam


class ScorpBot():
    def __init__(self):
        self.robot = Client()
        self.color_points = {}
        self.robot.close_gripper()
        self.calibrator = calibration.Translator2D()
        self.webcam = Webcam()

    def go_home(self):
        self.robot.home_robot()

    def calibrate(self):
        # TODO: Calibrate these points in advance before using.
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
        self.webcam.detect_all_colors()
        self.color_points = self.webcam.color_points()

    def touch_color_point(self, color):
        try:
            point = self.color_points.get(color)
            c = self.calibrator.transform_point(point)
            self.robot.teach_absolute_xyz_position(99, c[0], c[1], c[2], c[3], c[4])
            self.robot.move(99)
        except Exception as e:
            print e
