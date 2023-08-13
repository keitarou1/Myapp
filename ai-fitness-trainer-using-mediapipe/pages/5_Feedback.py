import streamlit_survey as ss
import streamlit as st
import json
survey = ss.StreamlitSurvey()
pages = survey.pages(1, on_submit=lambda: st.success("Your responses have been recorded. Thank you!"))
pages.submit_button = lambda pages: st.button("Submit", type="primary", use_container_width=True)
with pages:
    if pages.current == 0:
        st.write("Enter feedback")
        used_before = survey.radio(
            "Answers",
            options=["NA", "😞", "🙁", "😐", "🙂", "😀"],
            index=0,
            label_visibility="collapsed",
            horizontal=True,
        )
    if used_before =="😞":
        survey.text_input("Tell us why?"),
    if used_before =="😀":
        survey.text_input("Tell us why?"),




      
        


jsone = survey.to_json()
filename = 'C:/Users/ibrah/OneDrive/Skrivbord/programig/python/procjetct/Python trainer/ai-fitness-trainer-using-mediapipe/data.json'          #use the file extension .json
with open(filename, 'w') as file_object:  #open the file in write mode
 json.dump(jsone, file_object)  