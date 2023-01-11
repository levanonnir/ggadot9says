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
        self.color_points = self.webcam.color_points

    def touch_color_point(self, color):
        """
        This functino will touch the center of mass
        of a given color, as taken in the webcam's picture
        and as calculated by the Contour & ColorDetector classes.
        """
        try:
            point = self.color_points.get(color)
            print point
            c = self.calibrator.transform_point(point)
            print c
            self.robot.teach_absolute_xyz_position(40, c[0], c[1], 55, -107, -324)
            self.robot.move(40)
        except Exception as e:
            print e
