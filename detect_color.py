import cv2
import numpy as np

class ColorDetector():

    def __init__(self, path, color):
        self.color = color
        self.path = path

    def detect_color(self):  
        if self.color == "red":
            lower_bound = np.array([17, 15, 100], dtype = "uint8") # lower_red
            upper_bound = np.array([50, 56, 200], dtype = "uint8") # upper_red
        elif self.color == "blue":
            lower_bound = np.array([86, 31, 4], dtype = "uint8")  # lower_blue
            upper_bound = np.array([220, 88, 50], dtype = "uint8") # upper_blue
        elif self.color == "yellow":
            lower_bound = np.array([25, 146, 190], dtype = "uint8")  # lower_yellow
            upper_bound = np.array([62, 174, 250], dtype = "uint8") # upper_yellow
        elif self.color == "green":
            lower_bound = np.array([50, 20, 20], dtype = "uint8")  # lower_green
            upper_bound = np.array([100, 255, 255], dtype = "uint8") # upper_green
        elif self.color == "white":
            lower_bound = np.array([250, 250, 250], dtype = "uint8")  # lower_white
            upper_bound = np.array([255, 255, 255], dtype = "uint8") # upper_white
        elif self.color == "black":
            lower_bound = np.array([0, 0, 0], dtype = "uint8")  # lower_black
            upper_bound = np.array([0, 0, 0], dtype = "uint8") # upper_black
        
        image = cv2.imread(self.path)
        mask = cv2.inRange(image, lower_bound, upper_bound)
        detected_output = cv2.bitwise_and(image, image, mask =  mask)
        cv2.imshow(self.color, detected_output)
        cv2.imwrite("%s.jpg" % self.color, detected_output) 
        cv2.waitKey(0)

def main():
    color = input("What color? ").lower()
    detect = ColorDetector('image.jpg', color)
    detect.detect_color()

if __name__ == '__main__':
    main()