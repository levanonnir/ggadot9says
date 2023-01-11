import cv2
import numpy as np

class ColorDetector():
    """
    This class is used in order to detect a single color
    at each init.
    The lower and upper bounds have been set using the
    assistance_scripts/detect_color_hsv.py script.
    Look at the code example under the main function
    in order to understand how the class should be implemented.
    """
    def __init__(self, path, color):
        self.color = color
        self.path = path

    def detect_color(self):
        lower = None
        upper = None
        if self.color == "red":
            lower = np.array([0, 0, 255], dtype = "uint8") # lower_red
            upper = np.array([6, 204, 255], dtype = "uint8") # upper_red
        elif self.color == "blue":
            lower = np.array([86, 56, 119], dtype = "uint8")  # lower_blue
            upper = np.array([126, 255, 255], dtype = "uint8") # upper_blue
        elif self.color == "yellow":
            # lower_bound = np.array([25, 146, 190], dtype = "uint8")  # lower_yellow
            # upper_bound = np.array([62, 174, 250], dtype = "uint8") # upper_yellow
            lower = np.array([22, 93, 0], dtype = "uint8")
            upper = np.array([45, 255, 255], dtype = "uint8")
        elif self.color == "green":
            lower = np.array([50, 94, 177], dtype = "uint8")  # lower_green
            upper = np.array([86, 255, 255], dtype = "uint8") # upper_green
        elif self.color == "white":
            lower = np.array([250, 250, 250], dtype = "uint8")  # lower_white
            upper = np.array([255, 255, 255], dtype = "uint8") # upper_white
        elif self.color == "black":
            lower = np.array([0, 0, 0], dtype = "uint8")  # lower_black
            upper = np.array([0, 0, 0], dtype = "uint8") # upper_black
        elif self.color == "nothing":
            return
        
        image = cv2.imread(self.path)
        original = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # lower = np.array([22, 93, 0], dtype="uint8")
        # upper = np.array([45, 255, 255], dtype="uint8")
        mask = cv2.inRange(image, lower, upper)

        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(original, (x, y), (x + w, y + h), (36, 255, 12), 2)

        cv2.imshow('mask', mask)
        cv2.imshow('original', original)
        cv2.waitKey()

        # mask = cv2.inRange(image, lower_bound, upper_bound)
        detected_output = cv2.bitwise_and(image, image, mask=mask)
        cv2.imshow(self.color, detected_output)
        cv2.imwrite("%s.jpg" % self.color, detected_output) 
        cv2.waitKey(0)

def main():
    color = input("What color? ").lower()
    detect = ColorDetector('image.jpg', color)
    detect.detect_color()

if __name__ == '__main__':
    main()