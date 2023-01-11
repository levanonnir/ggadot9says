import cv2
import numpy as np
from pdb import set_trace
class DetectColor():
    """
    Dynamic tracking system. The user chooses with the left button of the mouse which
    color to track.
    Parameters: None.
    Return: None.
    """	
    def __init__(self):
        cv2.namedWindow('img')
        cv2.setMouseCallback('img',self.get_color)
        #Variable that enable the tracking only after the first click.
        self.firstClick=False

    def get_color(self,event,x,y,flags,param):
        #if left mouse was clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            self.x=x
            self.y=y
            self.firstClick=True
            #Variable that enable the computation of the color to track only once
            #after each click
            self.notClickedYet = True

    def main(self):
        #Enable video
        cap = cv2.VideoCapture(0)
        while True:
            #Read from camera
            _, frame = cap.read()
            #Show stream on 'img' window
            cv2.imshow('img', frame)
            #Wait to show stream
            k = cv2.waitKey(1) & 0xFF
            #Escape breaks the code
            if k==27:
                cv2.destroyAllWindows()
                break
            if self.firstClick:
                #Convert image to hsv format.
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # set_trace()
                if self.notClickedYet:
                    #Lower bound is determined by taking the h value and subtracting 10
                    #and s and v values are fixed to 50
                    lower=np.array([hsv[self.y][self.x][0]-10,50,50])
                    #Upper bound is determined by taking the h value and adding 10
                    #and s and v values are fixed to 255
                    upper=np.array([hsv[self.y][self.x][0]+10,255,255])
                    self.notClickedYet=False
                #Mask of 0 and 1 of the pixels within the range between lower and upper
                mask = cv2.inRange(hsv, lower, upper)
                #Apply the mask to the original pic
                res = cv2.bitwise_and(frame,frame, mask= mask)
                #Show the mask
                cv2.imshow('mask',mask)
                #Show the tracked color
                cv2.imshow('res',res)
        cv2.destroyAllWindows()

detect=DetectColor()
detect.main()
