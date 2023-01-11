from globals import COLORS
from save_pic import save_pic
from detect_color import ColorDetector
from contour import Contour

class Webcam:
    def __init__(self):
        self.image_path = "capture.jpg"
        save_pic(self.image_path, flag=1)
        self.color_points = {}
    
    def detect_all_colors(self):
        # Create a list of colors that are relevant for searching:
        valid_colors = list(COLORS.values())
        valid_colors.remove("black")
        valid_colors.remove("white")
        valid_colors.remove("nothing")
        for color in valid_colors:
            detector = ColorDetector(self.image_path, color)
            detector.detect_color()
            cont=Contour('%s.jpg' % color, 1)
            self.color_points[color] = cont.get_cm()[0]
            cont.show()



