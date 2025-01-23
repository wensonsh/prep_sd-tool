import json
import os

import streamlit as st

from utils import generate_random_id

st.session_state.clear()
st.set_page_config(page_title="Welcome", menu_items={'Get Help': 'mailto:wendi.shu@stud.tu-darmstadt.de'})
# Initialize session state for navigation and participant ID
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "welcome"
if "participant_id" not in st.session_state:
    st.session_state["participant_id"] = None

# Navigation function
def go_to_page(page_name):
    st.switch_page(page_name)

# Welcome Page
if st.session_state["current_page"] == "welcome":
    st.title("Welcome to the Generative AI Experiment")

    st.write("""
    This experiment explores the use of Generative AI (GenAI) tools in software development.
    You will be guided through this experiment. If you face any problems or in case you've got questions, feel free to contact wendi.shu@stud.tu-darmstadt.de.
    """)

    st.empty()

    st.write("If you are here for the first time, please click the 'Start' button.")

    if st.button("Start"):
        # Generate a new Participant ID and initialize their data
        participant_id = generate_random_id()
        st.session_state["participant_id"] = participant_id
        data = {
            "id": participant_id
        }
        if not os.path.exists("data/participants/participant_" + participant_id + ".json"):
            with open("data/participants/participant_" + participant_id + ".json", "w") as file:
                json.dump(data, file)
        st.switch_page("pages/init_survey.py")



    st.write("If you've already been here and want to continue, please enter your participant ID and click the 'Continue →' button.")
    input_id = st.text_input("Enter your Participant ID to continue:")
    if st.button("Continue →"):
        if not os.path.exists("data/participants/participant_" + input_id + ".json"):
            st.warning("ID not found. Please try again.")
        else:
            try:
                with open("data/participants/participant_" + input_id + ".json", "r") as f:
                    data = json.load(f)
            except FileNotFoundError:
                st.switch_page("app.py")

            if "next_page" in data:
                next_page = data["next_page"]
            else:
                next_page = "init_survey.py"

            st.session_state["participant_id"] = input_id
            st.switch_page("pages/" + next_page)

# Demographic Survey Page
elif st.session_state["current_page"] == "init_survey":
    pass

# Persona Survey Page
elif st.session_state["current_page"] == "persona_survey":
    pass

# Explanation Page
elif st.session_state["current_page"] == "experiment_explanation":
    pass

# gen_ai_tool Page
elif st.session_state["current_page"] == "gen_ai_tool":
    pass