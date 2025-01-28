import json

import streamlit as st

from pages.helper.file_helper import write_json
from pages.helper.navigation import home, back

st.set_page_config(page_title="Baseline Survey pt. 1", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})


FILE_PATH = "data/participants/"

# go to start if no session state
if 'participant_id' not in st.session_state:
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
if "solution_generate" not in data:
    back("pages/procedure.py")
elif "age" not in data:
    back("pages/post_survey.py")

data["finished"] = True
write_json(FILE_PATH, participant_id, data)

st.title("Finish")
st.markdown("""You have successfully completed the experiment. Thank you so much for your participation!""")
st.text("If you wish to continue using the GenAI tool that has been provided to you during this experiment, feel free to revisit the tool by entering your personal ID in the text field on the home page.")
st.text("Your personal ID is:")
st.code(participant_id)

st.text("")
st.divider()
if st.button("Back to home page 🏠︎"):
    home()