from globals import COLORS
from save_pic import save_pic
from detect_color import ColorDetector
from contour import Contour

class Webcam:
    def __init__(self):
        self.image_path = "images/capture.jpg"
        save_pic(self.image_path, flag=1)
        self.color_points = {}
    
    def detect_all_colors(self):
        """
        Detect all colors that exist within the NXT RoboLego
        sensor's spectrum within the webcam's view, and save
        each color's center of mass to self.color_points
        as a dictionary with the format {"color": (x,y)}.
        Please note that the values of black, white and nothing
        have been removed in order to prevent problems with the
        background used within the CIM Lab.
        """
        # Create a list of colors that are relevant for searching:
        valid_colors = list(COLORS.values())
        valid_colors.remove("black")
        valid_colors.remove("white")
        valid_colors.remove("nothing")
        for color in valid_colors:
            detector = ColorDetector(self.image_path, color)
            detector.detect_color()
            cont=Contour('images/%s.jpg' % color, 1)
            self.color_points[color] = cont.get_cm()[0]
            cont.show()



