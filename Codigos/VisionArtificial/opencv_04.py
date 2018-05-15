import numpy as np
import cv2
 
 
def main():
    
    #Funciones cv2.line(), cv2.circle() , cv2.rectangle(), cv2.ellipse(), cv2.putText()
    
    #Creamos un array 
    img = np.zeros((512,512,3), np.uint8)
     
    img = cv2.line(img,(0,0),(511,511),(255,0,0),50)
        
    img = cv2.circle(img,(447,63), 65, (0,0,255), -1)
    
    img = cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)
    
    img = cv2.ellipse(img,(256,300) ,(100,50),0,0,360,(0,255,0),-1)
    
    pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
    pts = pts.reshape((-1,1,2))
    img = cv2.polylines(img,[pts],True,(255,255,255))
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'Hackers e Ingenieros',(10,500), font, 1.5,(0,255,0),2,cv2.LINE_AA)
    
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
 
 
    return


 
 
if __name__ == '__main__':
    main()