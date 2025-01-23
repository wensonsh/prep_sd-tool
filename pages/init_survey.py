import json

import streamlit as st

st.set_page_config(page_title="Baseline Survey pt. 1", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})
# go to start if no session state
if 'participant_id' not in st.session_state:
    st.switch_page("app.py")
id = st.session_state["participant_id"]

# display participant ID as info box
st.info("Your participant ID: " + id + ".\n\nYou can use this id to return back in case you cannot complete the experiment in one go.")


try:
    with open("data/participants/participant_" + id + ".json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.switch_page("app.py")

def forward():
    if 'age' in data and 'job' in data and 'chat_gpt_proficiency' in data and 'chat_gpt_usage_private' in data and 'chat_gpt_usage_work' in data:
        st.switch_page("pages/persona_survey.py")
def back():
    st.switch_page("app.py")

st.title("Baseline Survey")
st.markdown("Please fill out the following form to help us understand your background and experience with ChatGPT.")

def validate_form(age, job, chat_gpt_proficiency, chat_gpt_usage_private, chat_gpt_usage_work):
    errors = {}
    if not age:
        errors["age"] = "Please enter your age"
    if not job:
        errors["job"] = "Please enter your job"
    if not chat_gpt_proficiency or chat_gpt_proficiency is None:
        errors["chat_gpt_proficiency"] = "Please enter your proficiency with ChatGPT"
    if not chat_gpt_usage_private:
        errors["chat_gpt_usage_private"] = "Please enter your usage frequency of GenAI tools like ChatGPT"
    if not chat_gpt_usage_work:
        errors["chat_gpt_usage_work"] = "Please enter your usage frequency of GenAI tools like ChatGPT or Copilot at work"

    return errors

#AGE
if "age" in data and data['age']:
    age = st.number_input("Your Age*", value = int(data['age']), min_value=0, max_value=100, step=1, key="age")
else:
    age = st.number_input("Your Age*", min_value=0, max_value=100, step=1, key="age")

#JOB
if "job" in data and data['job']:
    job = st.text_input("What is your current occupation?*", value = data['job'], key = "job")
else:
    job = st.text_input("What is your current occupation?*",  key = "job")

# LLM proficiency
chat_gpt_proficiency_values = ["Beginner", "Intermediate", "Advanced", "Expert"]
chat_gpt_proficiency_index = None

if "chat_gpt_proficiency" in data and data['chat_gpt_proficiency']:
    chat_gpt_proficiency_index = chat_gpt_proficiency_values.index(data["chat_gpt_proficiency"])

chat_gpt_proficiency = st.selectbox(
    label="How proficient are you with ChatGPT?*",
    options=chat_gpt_proficiency_values,
    index=chat_gpt_proficiency_index,
    placeholder="Please select"
)

# LLM usage private
chat_gpt_usage_values = ["never", "occasionally", "often", "(almost) every day"]
chat_gpt_usage_index = None

if "chat_gpt_usage_private" in data and data['chat_gpt_usage_private']:
    chat_gpt_usage_index = chat_gpt_usage_values.index(data["chat_gpt_usage_private"])

chat_gpt_usage_private = st.select_slider(
    label="How often do you use GenAI like ChatGPT for personal purposes?*",
    options=chat_gpt_usage_values
)

# LLM usage work
chat_gpt_usage_work_values = ["never", "occasionally", "often", "(almost) every day"]
chat_gpt_usage_work_index = None

if "chat_gpt_usage_work" in data and data['chat_gpt_usage_work']:
    chat_gpt_usage_work_index = chat_gpt_usage_work_values.index(data["chat_gpt_usage_work"])

chat_gpt_usage_work = st.select_slider(
    label="How often do you use GenAI like ChatGPT or Copilot for work purposes?*",
    options=chat_gpt_usage_work_values
)

left, middle, right = st.columns([12,8,4])
if right.button("Continue →", key="init_continue", type="primary"):
    # Clear previous error messages
    errors = validate_form(age, job, chat_gpt_proficiency, chat_gpt_usage_private, chat_gpt_usage_work)
    if errors:
        if "age" in errors:
            st.error(errors["age"])
        if "job" in errors:
            st.error(errors["job"])
        if "chat_gpt_proficiency" in errors:
            st.error(errors["chat_gpt_proficiency"])
        if "chat_gpt_usage_private" in errors:
            st.error(errors["chat_gpt_usage_private"])
        if "chat_gpt_usage_work" in errors:
            st.error(errors["chat_gpt_usage_work"])
    else:
        if age != 0:
            data['age'] = str(age)
        if job:
            data['job'] = job
        if chat_gpt_proficiency is not None:
            data['chat_gpt_proficiency'] = chat_gpt_proficiency
        if chat_gpt_usage_private is not None:
            data['chat_gpt_usage_private'] = chat_gpt_usage_private
        if chat_gpt_usage_work is not None:
            data['chat_gpt_usage_work'] = chat_gpt_usage_work


        data["next_page"] = "persona_survey.py"
        with open("data/participants/participant_" + id + ".json", "w") as f:
            json.dump(data, f)
        forward()

if left.button("← Back", key="back_app"):
    back()