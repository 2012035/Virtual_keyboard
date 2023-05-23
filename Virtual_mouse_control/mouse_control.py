import cv2
import mediapipe as mp
import time
import math
import numpy as np
import handTracking as ht
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

pTime=0
cTime=0



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
vol=volume.GetVolumeRange()
minvol=vol[0]
maxvol=vol[1]



video=cv2.VideoCapture(0)
video.set(3,480)
video.set(4,680)
video.set(10,150)
detection=ht.handDetector(detection=0.5)
while True:
    s,image=video.read()
    image=detection.handDetection(image,draw=False)
    list=detection.findPosition(image,draw=False)
    if len(list)!=0:
        x,y=list[4][1],list[4][2]
        x2,y2=list[8][1],list[8][2]
        x3,y3=list[12][1],list[12][2]
        cv2.circle(image,(x,y),5,(255,0,0),cv2.FILLED)
        cv2.circle(image, (x2, y2), 5, (255, 0, 0),cv2.FILLED)
        cv2.line(image,(x,y),(x2,y2),(255,0,0),4)
        cv2.circle(image,(int((x+x2)/2),int((y+y2)/2)),10,(255,230,0),cv2.FILLED)
        lenght=math.sqrt((x2-x)**2+(y2-y)**2)
        length1=math.sqrt((x3-x2)**2+(y3-y2)**2)
        if (lenght<=30):
            cv2.circle(image,(int((x+x2)/2),int((y+y2)/2)),10,(0,255,0),cv2.FILLED)

        vollen=np.interp(lenght,[20,180],[minvol,maxvol])
        if(length1>=50):
            volume.SetMasterVolumeLevel(vollen, None)



    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(image,str(int(fps)),(10,70) ,cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
    cv2.imshow('Mouse Volume Controll',image)
    if(cv2.waitKey(1) & 0xFF==ord('z')):
        break