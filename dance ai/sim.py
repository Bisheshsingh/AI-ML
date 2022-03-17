from scipy.io.wavfile import read
import numpy as np
import cv2,time
import mediapipe as mp

def text(s,img):
    cv2.putText(img,str(int(s)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

mdp=mp.solutions.pose
pose=mdp.Pose()
mpdraw=mp.solutions.drawing_utils

cap= cv2.VideoCapture('out.mp4')
cnt=0
pt=0
out=[]
while 1:
    suc,img=cap.read()
    print()
    im1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    res=pose.process(im1)
    var=230
    Lower_hsv = np.array([var for i in range(3)])
    Upper_hsv = np.array([255, 255, 255])
    mask= cv2.inRange(im1, Lower_hsv, Upper_hsv)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=0)
    lpoint,lpoint1=[],[]
    if res.pose_landmarks:
        mpdraw.draw_landmarks(img,res.pose_landmarks,mdp.POSE_CONNECTIONS)
        h,w,c=img.shape

        for id,lm in enumerate(res.pose_landmarks.landmark):
            lpoint1.extend([lm.x,lm.y])
            x,y=int(lm.x*w),int(lm.y*h)
            lpoint.append((x,y))
            cv2.circle(mask, center=(x,y), radius=0, color=(255,255,255), thickness=5)
        
        for i in mdp.POSE_CONNECTIONS:
            cv2.line(mask, lpoint[i[0]], lpoint[i[1]], color=(255,255,255), thickness=5)
       
        cv2.circle(mask, center=lpoint[0], radius=30, color=(255,255,255), thickness=5)
    
    cv2.imshow('mask',mask)
    #cv2.imshow('image',img)
    
    if cv2.waitKey(1)==27:
        break
    
cv2.destroyAllWindows()

