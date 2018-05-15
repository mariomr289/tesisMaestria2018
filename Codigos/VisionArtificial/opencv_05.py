import numpy as np
import cv2
 
 
drawing = False


def main():
    
    global img
    
    img = np.zeros((512,512,3), np.uint8)
        
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',draw_circle)
    
    while(1):
        cv2.imshow('image',img)
        
        k = cv2.waitKey(1) & 0xFF
        
        if k == 27:
            break
    
 
    return



# mouse callback function
def draw_circle(event,x,y,flags,param):
    
    global drawing
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True        

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(img,(x,y),5,(0,0,255),-1)
                
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False






 
 
if __name__ == '__main__':
    main()