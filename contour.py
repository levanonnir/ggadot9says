import cv2,numpy as np,math
class Contour():
    def __init__(self,path,n):
        self.path=path
        #Num objects
        self.n=n

    def compute(self):
        #Read image from path
        im=cv2.imread(self.path)
        #Convert to gray scale
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        #Convert to one bit above 127 white, below black
        ret, thresh = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY)
        #Find contours
        _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #Sort the contours in reverse order using Lambda, sorted,cv2.arcLength
        mmuyan=sorted(contours, key= lambda c : cv2.arcLength(c,True),reverse=True )
        #Declaire list of center of mases.
        self.cms=[]
        #Search only for a given num of objects
        for i in range(self.n):
            #Define a rectangle around each contour
            rect = cv2.minAreaRect(mmuyan[i])
            #Define a box 4 drawing
            box = cv2.boxPoints(rect)
            #Convert box points to integers (pixeles)
            box = np.int0(box)
            #Draw contours boundary on colored image
            self.pic = cv2.drawContours(im, [box], 0, (0, 0, 255), 2)
            #Get the momets dictionary
            M=cv2.moments(mmuyan[i])
            #Get x,y of the center of mass point.
            cx=int(M['m10']/M['m00'])
            cy=int(M['m01']/M['m00'])
            #Draw green circles on the centers.
            self.pic=cv2.circle(self.pic,(cx,cy),3,(0,255,0),2)
            #Add the center point to the list
            self.cms.append((cx,cy))

    def show(self):
        #Compute the center of mass for desired num of objects
        self.compute()
        #Show the result as a picture
        
        cv2.imshow('pic',self.pic)
        #Wait untill button is pressed
        cv2.waitKey(0)
        #Clear memory.
        cv2.destroyAllWindows()

    def get_cm(self):
        #Compute the center of mass for desired num of objects
        self.compute()
        #Return list with all center of mases.
        return self.cms

if __name__ == '__main__':
    cont=Contour('color detection.jpg',1)
    cont.show()
    print(cont.get_cm())
