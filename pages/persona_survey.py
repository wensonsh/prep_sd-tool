import json

import streamlit as st

#@TODO: only show this page if participant actually has ever used GenAI tools


st.set_page_config(page_title="Baseline Survey pt. 2", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})

# go to start if no session state
if 'participant_id' not in st.session_state:
    st.switch_page("app.py")
id = st.session_state["participant_id"]

# display participant ID as info box
st.info("Your participant ID: " + id + ".\n\nYou can use this id to return back in case you cannot complete the experiment in one go.")

#open the file of the user
try:
    with open("data/participants/participant_" + id + ".json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.switch_page("app.py")


def forward():
    #if 'age' in data and 'job' in data and 'chat_gpt_proficiency' in data and 'chat_gpt_usage' in data:
    st.switch_page()
def back():
    st.switch_page("pages/init_survey.py")

st.title("Baseline Survey pt. 2")
st.markdown("Please fill out the following form to help us understand your background, experience and preferences with ChatGPT and ChatGPT interactions.")

def validate_form(chat_gpt_answer_pref):
    errors = {}
    if not chat_gpt_answer_pref:
        errors["chat_gpt_answer_pref"] = "Please enter your ChatGPT answer preference."
    return errors


chat_gpt_answer_pref_values = ["As short as possible", "Short, but with explanations", "Long and with comprehensive explanations", "It depends on the task and context"]
chat_gpt_answer_pref_index = None
if "chat_gpt_answer_pref" in data and data['chat_gpt_answer_pref']:
    chat_gpt_answer_pref_index = chat_gpt_answer_pref_values.index(data["chat_gpt_answer_pref"])

chat_gpt_answer_pref = st.selectbox(
    label="In general, I prefer ChatGPT answers to be ...",
    options=chat_gpt_answer_pref_values,
    index=chat_gpt_answer_pref_index,
    placeholder="Select an option"
)

left, middle, right = st.columns([12,8,4])
if right.button("Continue →", key="continue_persona", type="primary"):
    # Clear previous error messages

    errors = validate_form(chat_gpt_answer_pref)
    if errors:
        if "chat_gpt_answer_pref" in errors:
            st.error(errors["chat_gpt_answer_pref"])
    else:
        if chat_gpt_answer_pref:
            data['chat_gpt_answer_pref'] = str(chat_gpt_answer_pref)


        data["next_page"] = "procedure.py"
        with open("data/participants/participant_" + id + ".json", "w") as f:
            json.dump(data, f)
        forward()

if left.button("← Back", key="back_persona"):
    back()