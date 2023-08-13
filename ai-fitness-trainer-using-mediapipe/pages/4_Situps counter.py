import cv2
import mediapipe as mp
import streamlit as st
import situps
FRAME_WINDOW = st.image([])
st.title("Site ups counter")

run =st.button("run")
stop= st.button("Stop")

cap = cv2.VideoCapture(0) 
situps_counter = situps.SitupsCounter()
# Open the default camera
if run:
    while True:
        ret, frame = cap.read()
        width  = cap.get(3)  # float `width`
        height = cap.get(4) 
        results = situps_counter.pose.process(frame)
        if results.pose_landmarks:
            
            situps_counter.detect_situp(results.pose_landmarks.landmark)
            situp_count = situps_counter.situp_count

            cv2.putText(frame, f"Sit-ups: {situp_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            situps_counter.mp_drawing.draw_landmarks(frame, results.pose_landmarks, situps_counter.mp_pose.POSE_CONNECTIONS)
        FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


        if stop:
            break

cap.release()
cv2.destroyAllWindows()

