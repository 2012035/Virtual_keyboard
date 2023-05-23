import cv2
import mediapipe as mp
import time
class handDetector():

    def __init__(self,mode=False,handNo=2,comple=1,detection=0.5,tracking=0.5):

        self.mode = mode
        self.handNo = handNo
        self.comple = comple
        self.detection = detection
        self.tracking = tracking
        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(self.mode,self.handNo,self.comple, self.detection, self.tracking)
        self.draw = mp.solutions.drawing_utils

    def handDetection(self,image,draw=True):
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.result=self.hands.process(rgb)
        if self.result.multi_hand_landmarks:
            for point in self.result.multi_hand_landmarks:
                    if draw:
                         self.draw.draw_landmarks(image,point,self.mpHand.HAND_CONNECTIONS)
        return image

    def findPosition(self,image,hand=0,draw=True):
        listPostion=[]
        if self.result.multi_hand_landmarks:
            my=self.result.multi_hand_landmarks[hand]
            for id, lm in enumerate(my.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    listPostion.append([id,cx,cy])
                    if draw:
                        cv2.circle(image,(cx,cy),5,(0,0,0),cv2.FILLED)
        return listPostion
def main():
 cTime = 0
 pTime = 0
 video = cv2.VideoCapture(0)
 detector=handDetector()
 while True:
     s, image = video.read()
     image=detector.handDetection(image)
     list=detector.findPosition(image)
     if len(list)!=0:
         print(list[1])
     cTime = time.time()
     fps = 1 / (cTime - pTime)
     pTime = cTime

     cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
     cv2.imshow('Output', image)
     if (cv2.waitKey(1) & 0xff == ord('z')):
         break


if __name__=="__main__":
    main()

