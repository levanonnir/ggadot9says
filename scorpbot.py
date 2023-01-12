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
        try:
            p1 = (370, 261)  # Green
            p2 = (299, 187)  # Red
            p3 = (368, 120)  # Yellow
            self.robot.teach_absolute_xyz_position(1, 212, 106, 13, -92, -7)  # Green
            q1 = self.robot.get_position_coordinates(1)
            self.robot.teach_absolute_xyz_position(10, 268, 143, 10, -92, -2)  # Red
            q2 = self.robot.get_position_coordinates(10)
            self.robot.teach_absolute_xyz_position(20, 304, 90, 11, -92, -2)  # Yellow
            q3 = self.robot.get_position_coordinates(20)
            self.calibrator.calibration(p1, p2, p3, q1, q2, q3)
            self.webcam.detect_all_colors()
            self.color_points = self.webcam.color_points
        except Exception as e:
            print "Error in calibration"
            print e

    def touch_color_point(self, color):
        """
        This function will touch the center of mass
        of a given color, as taken in the webcam's picture
        and as calculated by the Contour & ColorDetector classes.
        """
        try:
            point = self.color_points.get(color)
            print point
            c = self.calibrator.transform_point(point)
            print c
            self.robot.teach_absolute_xyz_position(4, c[0], c[1], 13, -92, -2)
            self.robot.teach_relative_xyz_position(40, 0, 0, 50, 0, 0, 4)
            self.robot.move(40)
            self.robot.move(4)
        except Exception as e:
            print e
