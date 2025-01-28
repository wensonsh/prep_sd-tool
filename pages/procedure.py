import json

import streamlit as st

from pages.helper.navigation import forward, home, get_header
from pages.helper.random_assignments import assign_to_group

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

# save group in session state
if "assigned_group" not in st.session_state:
    if "assigned_group" not in data:
        assigned_group = assign_to_group(participant_id)
        st.session_state["assigned_group"] = assigned_group
        data["assigned_group"] = assigned_group
    else:
        st.session_state["assigned_group"] = data["assigned_group"]
        assigned_group = data["assigned_group"]
else:
    assigned_group = st.session_state["assigned_group"]

get_header(2, "pages/init_survey.py", False, False, None, None)


IMAGE_PATH_DEFAULT = "resources/procedure/gen_ai_tool_default.png"
IMAGE_PATH_TAILORED = "resources/procedure/gen_ai_tool_tailored.png"

st.title("Procedure")
task = "write code based on a given task"
st.markdown("On the following page, you will be given a task and a GenAI assistant that you are supposed to use in order to solve the task.")

st.markdown("Please solve the task by submitting Python code in the solution box. The next page will be divided into three sections from left to right as depicted below (task description, GenAI chat, and solution section):")
if st.session_state["assigned_group"] == "group_default":
    st.image(IMAGE_PATH_DEFAULT, use_container_width=True)
elif st.session_state["assigned_group"] == "group_tailored":
    st.image(IMAGE_PATH_TAILORED, use_container_width=True)
st.markdown("To solve the task, please use the GenAI tool that is provided to you in the middle section of the page.")
if assigned_group == "group_tailored":
    st.markdown("""You will be able to adjust the interaction and response settings of the GenAI tool in the expander above the GenAI assistant. \nFurthermore, the tool already has all the context that you have, too:""")
    st.markdown("""
    - your task 
    - the information that you have entered in the previous survey
    """)
st.markdown("Please be aware, that the answers from the GenAI assistant are not always right. Feel free to change the settings above the GenAI assistant to adjust the interaction and response style.")
st.divider()
st.write("Your results will be saved as soon as you click on the 'Submit and continue' button on the right and you will be directed to the next page to conclude the experiment. "
         "You do not have to submit a correct answer, just try solving the task until you are satisfied. You should not take longer than 20 minutes, though.")
st.write("Happy collaboration! 🎉")
left, middle, right = st.columns([12,8,4])
if right.button("Continue →", key="init_continue", type="primary"):
     forward("pages/task.py", True, False, data, participant_id)
