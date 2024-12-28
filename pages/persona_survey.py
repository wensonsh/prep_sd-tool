import json

import streamlit as st

#@TODO: only show this page if participant actually has ever used GenAI tools


# go to start if no session state
if 'participant_id' not in st.session_state:
    st.switch_page("app.py")
id = st.session_state["participant_id"]

st.info("Your participant ID: " + id + ".\n\nYou can use this id to return back in case you cannot finish the experiment in one go.")

#open the file of the user
try:
    with open("data/user_" + id + ".json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    st.switch_page("app.py")


def forward():
    #if 'age' in data and 'job' in data and 'chat_gpt_proficiency' in data and 'chat_gpt_usage' in data:
    st.switch_page("pages/gen_ai_tool.py")
def back():
    st.switch_page("pages/init_survey.py")

st.title("Baseline Survey pt. 2")
st.markdown("Please fill out the following questions to help us understand your background, experience and preferences with ChatGPT and ChatGPT interactions.")

def validate_form(chat_gpt_answer_pref, familiar_programming_lang, familiar_programming_lang_exp):
    errors = {}
    if not chat_gpt_answer_pref:
        errors["chat_gpt_answer_pref"] = "Please enter your ChatGPT answer preference."
    if not familiar_programming_lang:
        errors["familiar_programming_lang"] = "Please select the programming language you are more familiar with."
    if not familiar_programming_lang_exp:
        errors["familiar_programming_lang_exp"] = "Please enter your proficiency with your more familiar programming language."

    return errors


chat_gpt_answer_pref_values = ["As short as possible", "Short, but with explanations", "Long and with comprehensive explanations", "It depends on the task and context"]
chat_gpt_answer_pref_index = None
if "chat_gpt_answer_pref" in data and data['chat_gpt_answer_pref']:
    chat_gpt_answer_pref_index = chat_gpt_answer_pref_values.index(data["chat_gpt_answer_pref"])

chat_gpt_answer_pref = st.selectbox(
    label="I prefer ChatGPT answers to be ...",
    options=chat_gpt_answer_pref_values,
    index=chat_gpt_answer_pref_index,
    placeholder="Select an option"
)

# Most familiar programming language
familiar_programming_langs_values = ["Java", "Python", "I'm equally good in both"]
familiar_programming_langs_index = None

if "familiar_programming_lang" in data and data['familiar_programming_lang']:
    familiar_programming_langs_index = familiar_programming_langs_values.index(data["familiar_programming_lang"])

familiar_programming_lang = st.radio(label = "Please select the programming language that you are more familiar with:",
                                     options=familiar_programming_langs_values,
                                     index=familiar_programming_langs_index)

# Experience
familiar_programming_lang_exp_values = ["Beginner", "Intermediate", "Advanced", "Expert"]
familiar_programming_lang_exp_index = None

if "familiar_programming_lang_exp" in data and data['familiar_programming_lang_exp']:
    familiar_programming_lang_exp_index = familiar_programming_lang_exp_values.index(data["familiar_programming_lang_exp"])

if (familiar_programming_lang):
    #proficiency statt years, weil years niht so aussagekräfitg, jenachdem wie oft man mit der lang zu tun hat [332]
    familiar_programming_lang_exp = st.selectbox(label="How would you describe your proficiency in " + familiar_programming_lang + "?",
                 options=familiar_programming_lang_exp_values,
                 index=familiar_programming_lang_exp_index)

left, middle, right = st.columns([12,8,4])
if right.button("Continue →", key="continue_persona"):
    # Clear previous error messages


    errors = validate_form(chat_gpt_answer_pref, familiar_programming_lang, familiar_programming_lang_exp)
    if errors:
        if "chat_gpt_answer_pref" in errors:
            st.error(errors["chat_gpt_answer_pref"])
        if "familiar_programming_lang" in errors:
            st.error(errors["familiar_programming_lang"])
        if "familiar_programming_lang_exp" in errors:
            st.error(errors["familiar_programming_lang_exp"])
    else:
        if chat_gpt_answer_pref:
            data['chat_gpt_answer_pref'] = str(chat_gpt_answer_pref)
        if familiar_programming_lang:
            data['familiar_programming_lang'] = familiar_programming_lang
        if familiar_programming_lang_exp:
            data['familiar_programming_lang_exp'] = familiar_programming_lang_exp


        data["next_page"] = "gen_ai_tool.py"
        with open("data/user_" + id + ".json", "w") as f:
            json.dump(data, f)
        forward()

if left.button("← Back", key="back_persona"):
    back()