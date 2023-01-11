import cv2,os

def save_pic(path='img1.jpg',flag=None):
    """
    Show stream s key save img q key aborts.
    parameters:
    path path 4 saving image
    flag flag to convert image
    """
    cap = cv2.VideoCapture(0)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        # Display the resulting frame
        cv2.imshow('frame',frame)
        # Wait for press
        w=cv2.waitKey(1) & 0xFF
        # Quit
        if w==ord('q'):
            break
        # Saving
        elif w==ord('s'):
            if flag:
                frame=cv2.cvtColor(frame, flag)
            #Save to disk.
            cv2.imwrite(path,frame)
    #Release memory.
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Run 'save_pic' function:
    save_pic(flag=1)