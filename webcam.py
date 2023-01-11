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
        for color in COLORS.values():
            detector = ColorDetector(color, self.image_path)
            detector.detect_color()
            cont=Contour('%s.jpg' % color, 1)
            self.color_points[color] = cont.get_cm()[0]
            cont.show()



