import cv2
class Config_Cam():
    """
    Build trackbar from list of attributes names for configuration.
    Parameters 3 lists:
        names: names of attributes of cam.
        values: current value of attribute
        counts: max values of attributes
    """
    def __init__(self,**dict):
        #Get list of names of attributes to config
        self.names=dict["names"]
        #Get list of values of attributes to config
        self.values=dict["values"]
        #Get list of counts of attributes to config
        self.counts=dict["counts"]
        #Predefine window name
        cv2.namedWindow('image')
        for i in range(len(self.names)):
            #Create trackbars from all the names each one is called with a
            #name from the list params(nameOfTrackbar,windowName,currentValue,countValue,callBackName)
            cv2.createTrackbar(self.names[i],'image',self.values[i],self.counts[i], self.on_track)

    def on_track(self,x):
        pass

    def main(self):
        cap = cv2.VideoCapture(0)
        #Define a dictionary that will hold the variables of the exact value
        #of the configed parameter
        myDic={}
        while True:
            _, self.img = cap.read()
            #Wait to show the image
            k = cv2.waitKey(10) & 0xFF
            #Escape breaks the program
            if k == 27:
                cv2.destroyAllWindows()
                break
            #Iterate names
            for n in (self.names):
                #Set value of dictionary to value of slider parameters name of bar, name of window
                myDic[n]=cv2.getTrackbarPos(n,'image')
                #Set the name of attribute in a way that opencv understand
                #for example:cv2.CAP_PROP_CONTRAST
                attr='cv2.CAP_PROP_'+n.upper()
                #Set the desired value to the camera, ranges of these attributes are 0:1
                #and the sliders values are 0:100 so we scale it by 1/100
                # the eval method change from string to object.
                cap.set(eval(attr),myDic[n])
            #Show video with configed cam on the predefined window parameters winName,frame
            cv2.imshow('image', self.img)

conf=Config_Cam(names=['Contrast','Saturation','Brightness'],values=[50,50,50],counts=[100,100,100])
conf.main()