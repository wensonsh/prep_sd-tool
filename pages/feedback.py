import json

import streamlit as st

from pages.helper.file_helper import write_json, open_json
from pages.helper.navigation import home, back

st.set_page_config(page_title="Feedback", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})


FEEDBACK_FILE_PATH = "data/feedback/"

# go to start if no session state
if 'participant_id' not in st.session_state:
    print("NOT IN SESS")
    home()
participant_id = st.session_state["participant_id"]

try:
    with open("data/participants/participant_" + participant_id + ".json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.switch_page("app.py")
except TypeError:
    st.switch_page("app.py")

# check if participant really finished the survey by checking the entries in the json file
if "exp_finished" not in data or not data["exp_finished"]:
    st.switch_page("app.py")

st.title("Feedback")
st.markdown("""Please provide feedback on your experience with this experiment. Your feedback is valuable to us and will help us improve the experiment for future participants.""")
feedback = st.text_area("Feedback", key="feedback", height=200)
if st.button("Submit feedback"):
    feedback_data = open_json(FEEDBACK_FILE_PATH, participant_id)
    feedback_data["feedback"] = feedback
    write_json(FEEDBACK_FILE_PATH, participant_id, feedback_data)
    st.success("Feedback submitted successfully! Thank you for your feedback.")
st.text("")
st.divider()
if st.button("Back to home page 🏠︎"):
    home()