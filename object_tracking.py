import cv2
import numpy as np 
"""
Tacks any moving object in frame
"""
cap = cv2.VideoCapture('video.webm')
#cap = cv2.VideoCapture(0) #uncomment the line to use your webcam
(camx,camy) = (640,520)

cap.set(3,camx)
cap.set(4,camy)


ret,frame1 = cap.read()
ret,frame2 = cap.read()


while(cap.isOpened()):
    
    frame_diff = cv2.absdiff(frame1,frame2)
    gray_img = cv2.cvtColor(frame_diff,cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray_img,(5,5),0)

    _,thresh = cv2.threshold(blur,25,255,cv2.THRESH_BINARY)

    dilate = cv2.dilate(thresh,None,iterations=5)
    erode = cv2.erode(dilate,None,iterations=4)


    contours , _ = cv2.findContours(erode,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    for contour in contours:
        (x,y,w,h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour)< 800:
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,0,255),6)
        cv2.putText(frame1,"MOVEMENT ",(20,40),cv2.FONT_HERSHEY_COMPLEX,2,(25,0,255),2)

    frame = cv2.resize(frame1,(600,400)) 
    
    cv2.imshow("tracking",frame)
    

    frame1 = frame2

    ret,frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
cap.release()