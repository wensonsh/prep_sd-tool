import json

import streamlit as st

st.set_page_config(page_title="Baseline Survey pt. 1", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})
# go to start if no session state
if 'participant_id' not in st.session_state:
    st.switch_page("app.py")
id = st.session_state["participant_id"]

# display participant ID as info box
st.info("Your participant ID: " + id + ".\n\nYou can use this id to return back in case you cannot complete the experiment in one go. But please mind, that from this page on, the next steps should be finished in one go.")


try:
    with open("data/participants/participant_" + id + ".json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.switch_page("app.py")

def forward():
    if 'age' in data and 'job' in data and 'chat_gpt_proficiency' in data and 'chat_gpt_usage_private' in data and 'chat_gpt_usage_work' in data:
        # st.switch_page("pages/gen_ai_tool.py")
        st.switch_page("pages/gen_ai_tool.py")
def back():
    st.switch_page("pages/persona_survey.py")
IMAGE_PATH = "resources/gen_ai_tool_labels.png"
st.title("Procedure")
task = "write code based on a given task"
st.write("Please put yourself in the following fictional situation:")
st.divider()
st.write("You are our new hire as software developer at company ExP. We are very happy to have you on board 🎉")
st.markdown("*After a little tour, an introduction, and organizational proceedings, you are given your first task which you will see on the next page.*")
st.markdown("*You are asked to {task}. The next page will be divided into three sections from left to right as depicted below:*")
st.image(IMAGE_PATH, use_container_width=True)
st.markdown("*In order to solve the task, please use the GenAI assistant that is provided to you in the middle section of the page. The GenAI assistant has all the context you will need to solve the task, including*")
st.markdown("""
- your task 
- the information that you have entered in the previous survey
- our company's best practices
""")
st.markdown("Though, please be aware, that the answers are not always right. Feel free to change the settings above the GenAI assistant to adjust the interaction style.")
st.divider()
st.write("Your results will be saved as soon as you click on the 'Submit' button on the right and you will be directed to the next page to conclude the experiment. "
         "You do not have to submit a correct answer, just try solving the task until you are satisfied. You should not take longer than 20 minutes, though.")

left, middle, right = st.columns([12,8,4])
if right.button("Continue →", key="init_continue", type="primary"):
    forward()

if left.button("← Back", key="back_persona_survey"):
    back()