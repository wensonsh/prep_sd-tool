import json

import streamlit as st

from pages.helper.random_assignments import assign_to_group
from pages.helper.timer import get_current_time
from pages.helper.navigation import forward, home, get_header

st.set_page_config(page_title="Baseline Survey pt. 1", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})

# go to start if no session state
if 'participant_id' not in st.session_state:
    home()
participant_id = st.session_state["participant_id"]

try:
    with open("data/participants/participant_" + participant_id + ".json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.switch_page("app.py")

try:
    # save group in session state
    if "assigned_group" not in st.session_state:
        assigned_group = assign_to_group(participant_id)
        st.session_state["assigned_group"] = assigned_group
        data["assigned_group"] = assigned_group
    else:
        st.session_state["assigned_group"] = data["assigned_group"]
except Exception:
    st.error("@TODO: fallback")

get_header(2, "pages/init_survey.py", False, False, None, None)


IMAGE_PATH = "resources/gen_ai_tool_labels.png"

st.title("Procedure")
task = "write code based on a given task"
st.markdown("On the following page, you will be given a task and a GenAI assistant that you are supposed to use in order to solve the task.")

st.markdown("*You are asked to {task}. The next page will be divided into three sections from left to right as depicted below:*")
st.image(IMAGE_PATH, use_container_width=True)
st.markdown("*In order to solve the task, please use the GenAI assistant that is provided to you in the middle section of the page. The GenAI assistant has all the context you will need to solve the task, including*")
st.markdown("""
- your task 
- the information that you have entered in the previous survey
""")
st.markdown("Though, please be aware, that the answers from the GenAI assistant are not always right. Feel free to change the settings above the GenAI assistant to adjust the interaction and response style.")
st.divider()
st.write("Your results will be saved as soon as you click on the 'Submit and continue' button on the right and you will be directed to the next page to conclude the experiment. "
         "You do not have to submit a correct answer, just try solving the task until you are satisfied. You should not take longer than 20 minutes, though.")
st.write("Happy collaboration! 🎉")
left, middle, right = st.columns([12,8,4])
if right.button("Continue →", key="init_continue", type="primary"):
    if 'age' in data and 'job' in data and 'chat_gpt_proficiency' in data and 'chat_gpt_usage_private' in data and 'chat_gpt_usage_work' in data:
        forward("pages/gen_ai_tool.py", True, False, data, participant_id)
