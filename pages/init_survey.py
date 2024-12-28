import json

import streamlit as st
from click import style

from pages.persona_survey import middle

# go to start if no session state
if 'participant_id' not in st.session_state:
    st.switch_page("app.py")
id = st.session_state["participant_id"]


st.info("Your participant ID: " + id + ".\n\nYou can use this id to return back in case you cannot finish the experiment in one go.")


try:
    with open("data/user_" + id + ".json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.switch_page("app.py")

def forward():
    if 'age' in data and 'job' in data and 'chat_gpt_proficiency' in data and 'chat_gpt_usage' in data:
        st.switch_page("pages/persona_survey.py")
def back():
    st.switch_page("app.py")

st.title("Baseline Survey")
st.markdown("Please fill out the following form to help us understand your background and experience with ChatGPT.")

def validate_form(age, job, chat_gpt_proficiency, chat_gpt_usage):
    errors = {}
    if not age:
        errors["age"] = "Please enter your age"
    if not job:
        errors["job"] = "Please enter your job"
    if not chat_gpt_proficiency or chat_gpt_proficiency is None:
        errors["chat_gpt_proficiency"] = "Please enter your proficiency with ChatGPT"
    if not chat_gpt_usage:
        errors["chat_gpt_usage"] = "Please enter your usage with ChatGPT"

    return errors

#AGE
if "age" in data and data['age']:
    age = st.number_input("Your Age", value = int(data['age']), min_value=0, max_value=100, step=1, key="age")
else:
    age = st.number_input("Your Age", min_value=0, max_value=100, step=1, key="age")

#JOB
if "job" in data and data['job']:
    job = st.text_input("Your Current Occupation", value = data['job'], key = "job")
else:
    job = st.text_input("Your Current Occupation",  key = "job")

# LLM proficiency
chat_gpt_proficiency_values = ["Beginner", "Intermediate", "Advanced", "Expert"]
chat_gpt_proficiency_index = None

if "chat_gpt_proficiency" in data and data['chat_gpt_proficiency']:
    chat_gpt_proficiency_index = chat_gpt_proficiency_values.index(data["chat_gpt_proficiency"])

chat_gpt_proficiency = st.selectbox(
    label="How proficient are you with ChatGPT?",
    options=chat_gpt_proficiency_values,
    index=chat_gpt_proficiency_index,
    placeholder="Select an option"
)

# LLM usage
chat_gpt_usage_values = ["Never", "1-2 times", "3-5 times", "More than 5 times"]
chat_gpt_usage_index = None

if "chat_gpt_usage" in data and data['chat_gpt_usage']:
    chat_gpt_usage_index = chat_gpt_usage_values.index(data["chat_gpt_usage"])

chat_gpt_usage = st.selectbox(
    label="How often have you used GenAI like ChatGPT in the past week?",
    options=chat_gpt_usage_values,
    index = chat_gpt_usage_index,
    placeholder="Select an option"
)

left, middle, right = st.columns([12,8,4])
if right.button("Continue →", key="init_continue"):
    # Clear previous error messages
    errors = validate_form(age, job, chat_gpt_proficiency, chat_gpt_usage)
    if errors:
        if "age" in errors:
            st.error(errors["age"])
        if "job" in errors:
            st.error(errors["job"])
        if "chat_gpt_proficiency" in errors:
            st.error(errors["chat_gpt_proficiency"])
        if "chat_gpt_usage" in errors:
            st.error(errors["chat_gpt_usage"])
    else:
        if age != 0:
            data['age'] = str(age)
        if job:
            data['job'] = job
        if chat_gpt_proficiency is not None:
            data['chat_gpt_proficiency'] = chat_gpt_proficiency
        if chat_gpt_usage is not None:
            data['chat_gpt_usage'] = chat_gpt_usage

        data["next_page"] = "persona_survey.py"
        with open("data/user_" + id + ".json", "w") as f:
            json.dump(data, f)
        forward()

if left.button("← Back", key="back_persona"):
    back()