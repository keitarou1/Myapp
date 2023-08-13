import cv2
import streamlit as st
import numpy as np
import mediapipe as mp
import PoseModule as pm
detector = pm.poseDetector()
count = 0
direction = 0
form = 0
feedback = "Fix Form"
st.title("Push ups counter")
FRAME_WINDOW = st.image([])
cap = cv2.VideoCapture(0)
run =st.button("run")
stop =st.button("stop")

if run:
    while True:
            ret, img = cap.read()
            width  = cap.get(3)  # float `width`
            height = cap.get(4)  # float `height`
            img = detector.findPose(img, False)
            lmList = detector.findPosition(img, False)
            # print(lmList)
            if len(lmList) != 0:
                elbow = detector.findAngle(img, 11, 13, 15)
                shoulder = detector.findAngle(img, 13, 11, 23)
                hip = detector.findAngle(img, 11, 23,25)
                
                #Percentage of success of pushup
                per = np.interp(elbow, (90, 160), (0, 100))
                
                #Bar to show Pushup progress
                bar = np.interp(elbow, (90, 160), (380, 50))

                #Check to ensure right form before starting the program
                if elbow > 160 and shoulder > 40 and hip > 160:
                    form = 1
            
                #Check for full range of motion for the pushup
                if form == 1:
                    if per == 0:
                        if elbow <= 90 and hip > 160:
                            feedback = "Up"
                            if direction == 0:
                                count += 0.5
                                direction = 1
                        else:
                            feedback = "Fix Form"
                            
                    if per == 100:
                        if elbow > 160 and shoulder > 40 and hip > 160:
                            feedback = "Down"
                            if direction == 1:
                                count += 0.5
                                direction = 0
                        else:
                            feedback = "Fix Form"
                                # form = 0
                        
                            
            
                
                #Draw Bar
                if form == 1:
                    cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                    cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 0, 0), 2)


                #Pushup counter
                cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                            (255, 0, 0), 5)
                
                #Feedback 
                cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
                cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                            (0, 255, 0), 2)

            
            FRAME_WINDOW.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            if stop:
                break
cap.release()
cv2.destroyAllWindows()
